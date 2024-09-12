// Algorithm:
//1. Token and User Type Check:

// Check for the presence of a token in localStorage. If no token is found, redirect the user to the login page.

// Determine the user's type and display or hide specific elements (standard-details) based on the user role (i.e., if the user is not staff, hide certain elements).


//2. Fetching Standard List:

// If the user is a staff member, a GET request is made to fetch a list of grades (standards) from the API.

// The response data (grades and sections) is stored in grade_list, and the standard-edit section becomes visible for further modification.


//3. Section Listing:

// When a standard is selected, the corresponding sections are displayed in a dropdown list.

// Profile Fetching and Display:

// Fetch the profile details using a GET request with the authentication token.

// Profile information such as name, standards, and address is displayed on the page.

// For staff members, the standard-edit section shows a list of standards and provides options to add or delete standards.


//4. Profile Editing:

// When the edit button is clicked, the form to edit the profile is displayed. The existing profile data is populated in the form fields.

// On form submission, a PUT request is made to update the profile details on the server. Once updated, the profile details are reloaded and shown on the page.

// start 
// Get the token and user details from localStorage

let token = localStorage.getItem("token")
var user = localStorage.getItem('user_type')
let container = document.querySelector('.container');
let messages = document.querySelector('.messages')
let error_messages = document.querySelector('.error-messages')
let grade_list = []
let form = document.getElementById('profile-box')
let csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
let content = ''
let data_entry = localStorage.getItem('data_entry')

// Check if token is available, if not redirect to login page
$(document).ready(function () {
  if (!token) {
    return window.location.href = '/login';
  }
  // Disable profile link if already on the profile page
  document.getElementById('nav-profile').style.opacity = '0.5';
})

// If the user is not staff, hide the standard-details section
if (user != 'is_staff') {
  document.getElementById('standard-details').style.display = 'none'
} else {
  // Fetch grades (standards) if the user is staff
  fetch('http://127.0.0.1:8000/api/grades/', {
    method: 'GET',
  }).then(res => {
    return res.json()
  }).then(data => {
    grade_list = data.data
    if (data.status == 'failure') {
      window.location.href = `${window.location.protocol}//${window.location.host}/404`
    }
    // Populate the standards dropdown
    content += `<option value="" selected="">---------</option>`
    if (grade_list.length) {
      document.getElementById('standard-edit').style.display = 'block'
      for (let i = 0; i < grade_list.length; i++) {
        content += `<option value="${grade_list[i].grade}">${grade_list[i].grade}</option>`
      }
    }
    document.querySelector('.std-in-form').innerHTML = content
  })
}

// Function to get the list of sections based on selected standard
function getsectionname(element) {
  let standard = element.value
  let sec_list;
  content = ''
  for (let i = 0; i < grade_list.length; i++) {
    if (grade_list[i].grade == standard) {
      sec_list = grade_list[i].section
    }
  }
  content += `<option value="" selected="">---------</option>`
  if (sec_list && sec_list.length) {
    for (let i = 0; i < sec_list.length; i++) {
      content += `<option value="${sec_list[i]}">${sec_list[i]}</option>`
    }
  }
  document.querySelector('.sec-in-form').innerHTML = content
}

// Function to delete a standard from the staff user's list
function delete_standard(index) {
  standards.splice(index, 1); // Remove the standard from the list
  let content = '<p> standards list</p>'
  for (let i = 0; i < standards.length; i++) {
    content += `<li>${standards[i]} <button onclick=delete_standard(${i})>delete</button></li>`
  }
  document.querySelector('.standard-edit').innerHTML = content
}

// Function to add a new standard and section to the list
function add() {
  let std = document.getElementById('std').value
  let section = (document.getElementById('sec').value).toUpperCase()

  // Validation for valid section input
  if (!section.match(/[a-z]/i)) {
    document.querySelector('.profile-errors').innerHTML = '<li class="text-danger">give a valid section</li>'
    return
  }

  // Avoid adding duplicate standard-section combinations
  if (!standards.includes(std + '-' + section)) {
    standards.push(std + '-' + section)
  } else {
    document.querySelector('.profile-errors').innerHTML = '<li class="text-danger">standard and section already added</li>'
    return
  }

  // Update the list in the HTML
  let content = '<p> standards list</p>'
  for (let i = 0; i < standards.length; i++) {
    content += `<li>${standards[i]} <button onclick=delete_standard(${i})>delete</button></li>`
  }
  document.querySelector('.standard-edit').innerHTML = content
}

// Function to fetch and display user profile details
function profile() {
  if (token) {
    fetch('http://127.0.0.1:8000/api/profile/', {
      method: 'GET',
      headers: new Headers({
        'Authorization': 'token' + ' ' + token,
        'Content-Type': 'application/x-www-form-urlencoded',
      })
    })
      .then(response => response.json())
      .then(data => {
        let htmlSegment = `
          <div class="user d-flex flex-wrap flex-column" id='${data.data.id}'>
            <div class="profile-head">
              <div class='image'>
                <img src='http://127.0.0.1:8000/${data.data.profile?.profile_picture}'>
              </div>
              <p class="fullname">${data.data.profile?.full_name}</p><br>`

        // For non-student users, show standards list
        if (user != 'is_student') {
          let content = '<p> standards list</p>'
          standards = data.data.profile?.standard
          for (let i = 0; i < standards.length; i++) {
            content += `<li>${standards[i]} <button onclick=delete_standard(${i})>delete</button></li>`
          }
          document.querySelector('.standard-edit').innerHTML = content
        }

        // Display user type information
        if(user != ''){
          htmlSegment += `<p class ='occupation'>${user.slice(3)}</p>`
          }
          else if(data_entry){
            htmlSegment += `<p class ='occupation'>data entry operator</p>`
          }
          htmlSegment +=   `</div>
         <div class="profile-content">
         <p><label class=profile-label>First Name:</label><span  class="firstname">${data.data.profile?.first_name}</span></p>
         <p><label class=profile-label>Last Name:</label><span class="lastname">${data.data.profile?.last_name}</span></p>`
         if(data.data.profile?.standard.length == 1){
          htmlSegment +=     `<p> <label class=profile-label>Standard:</label><span  class="std">${data.data.profile?.standard}</span></p>`
         }
         else if(data.data.profile?.standard.length > 1){
          htmlSegment +=     `<p> <label class=profile-label>Standard:</label>`
          for (let i = 0; i < data.data.profile?.standard.length; i++) {
           htmlSegment += `<li> ${data.data.profile?.standard[i]} </li>`
          }
         htmlSegment += `</p>`
         }
  
         htmlSegment +=   `<p> <label class=profile-label>Address: </label><span class="address">${data.data.profile?.address}</span></p>
  
              <i id='profile-edit' class="fa fa-edit"></i>
              </div>`;
  container.innerHTML = htmlSegment;
        })
    }
  }
  
  // profile edit function
  container.addEventListener('click', (e) => {
    fname = document.getElementById('fname');
    lname = document.getElementById('lname');
    ffname = document.getElementById('ffname');
    // std= document.getElementById('std');
    // sec= document.getElementById('sec');
    ad = document.getElementById('address');
    button = document.getElementById('profile-btn')
    e.preventDefault();
    let editbutton = e.target.id == 'profile-edit';
    let id = e.target.parentElement.parentElement.id;
    console.log(id)
    if (editbutton) {
      form.style.display = 'block'
      container.style.display = 'none'
      console.log('hi')
      url = "http://127.0.0.1:8000/api/student-profile/"
      const parent = e.target.parentElement;
      console.log(parent)
      let fullname = parent.parentElement.querySelector('.fullname').textContent;
      let lastname = parent.querySelector('.lastname').textContent;
      let firstname = parent.querySelector('.firstname').textContent;
      // let standard= parent.querySelector('.std').textContent;
      // let section= parent.querySelector('.sec').textContent;
      let address = parent.querySelector('.address').textContent;
      document.getElementById('ffname').value = fullname
      document.getElementById('lname').value = lastname
      document.getElementById('fname').value = firstname
      // document.getElementById('std').value=standard
      // document.getElementById('sec').value=section
      document.getElementById('address').value = address
      button.addEventListener('click', () => {
        fetch(`${url}${id}/`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'token' + " " + localStorage.getItem('token'),
            'X-CSRFToken': csrftoken
          },
          body: JSON.stringify(
            { 'first_name': fname.value, 'last_name': lname.value, 'standard': standards, 'full_name': ffname.value, 'address': ad.value }
          )
        }).then(response => {
          if (response.status == 200) {
            console.log("Sucess response", response)
            messages.innerHTML = 'updated successfully'
            error_messages.innerHTML = ''
            fetch('http://127.0.0.1:8000/api/profile/', {
              method: 'GET',
              headers: {
                'content-Type': 'application/json',
                'Authorization': 'token' + ' ' + token,
              }
            }).then(res => {
              return res.json()
            }).then(d => {
              if (d.data.profile.standard) {
                localStorage.setItem("standard", d.data.profile.standard);
              }
              profile();
            })
          } else {
            error_messages.innerHTML = `<li>${(data.data.error)}</li>`
            messages.innerHTML = ''
          }
          form.style.display = 'none'
          container.style.display = 'block'
          return response.json();
        }).then(function (data) {
          console.log(data)
          // if (data.status != 'success'){
          // error_messages.innerHTML = `<li>${(data.data.error)}</li>`
          // messages.innerHTML = ''
          // }
        })
      })
    }
  }
  
  );
  profile();