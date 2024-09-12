let token = localStorage.getItem("token")
var user = localStorage.getItem('user_type')
var host = window.location.protocol + "//" + window.location.host;
let container = document.querySelector('.container');
let messages = document.querySelector('.messages')
let error_messages = document.querySelector('.error-messages')
let standards, get_standard;
let form = document.getElementById('profile-box')
let csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
let content = ''
let grade_list = []
let data_entry = localStorage.getItem('data_entry')


// user check
$(document).ready(function () {
  if (!token) {
    return window.location.href = '/login';
  }
  document.getElementById('nav-profile').style.opacity = '0.5';
})

if (user != 'is_staff') {
  document.getElementById('standard-details').style.display = 'none'
} else {
  fetch('http://127.0.0.1:8000/api/grades/', {
    method: 'GET',
  }).then(res => {
    return res.json()
  }).then(data => {
    grade_list = data.data
    console.log(data.data)
    if (data.status == 'failure') {
      window.location.href = `${host}/404`
    }
    content += ` 
          <option value="" selected="">---------</option>`
    if (grade_list.length) {
   
      // if(user !='is_staff' && !data_entry){
      //   document.getElementById('standard-edit').style.display = 'block'
      // }
      document.getElementById('standard-edit').style.display = 'block'
      for (i = 0; i < grade_list.length; i++) {
        content += ` <option value="${grade_list[i].grade}">${grade_list[i].grade}</option>`
      }
    }
    document.querySelector('.std-in-form').innerHTML = content
  })
}

if (!grade_list.length) {
  document.getElementById('standard-edit').style.display = 'none'
}
// 

// section listing function
function getsectionname(element) {
  let standard = element.value
  let sec_list;
  content = ''
  for (i = 0; i < grade_list.length; i++) {
    if (grade_list[i].grade == standard) {
      sec_list = grade_list[i].section
    }
  }
  content += ` 
          <option value="" selected="">---------</option>`
  if (sec_list && sec_list.length) {
    for (i = 0; i < sec_list.length; i++) {
      content += ` <option value="${sec_list[i]}">${sec_list[i]}</option>`
    }
  }
  document.querySelector('.sec-in-form').innerHTML = content
}

// profile edit back function
function back() {
  form.style.display = 'none'
  container.style.display = 'block'
}

// remove standard from staff user standard list
function delete_standard(index) {
  standards.splice(index, 1);
  let content = ''
  content += `    <p> standards list</p>`
  for (i = 0; i < standards.length; i++) {
    content += `<li>${standards[i]} <button onclick=delete_standard(${i})>delete</button></li>`
  }
  // content += `<input type="number" id="std" placeholder="Standard">
  // <label >Section:</label><br><input type="text" id="sec" placeholder="section">
  // <button onclick=add()>add</button>
  // <hr>
  // `
  document.querySelector('.standard-edit').innerHTML = content
}

// add standard from staff user standard list
function add() {
  let std = document.getElementById('std').value
  let section = (document.getElementById('sec').value).toUpperCase()
  if (!section.match(/[a-z]/i)) {
    document.querySelector('.profile-errors').innerHTML = '<li class="text-danger">give a valid section</li>'
    return
  }
  if (!standards.includes(std + '-' + section)) {
    standards.push(std + '-' + section)
  } else {
    document.querySelector('.profile-errors').innerHTML = '<li class="text-danger">standard and section altready added</li>'
    return
  }
  let content = ''
  content += `    <p> standards list</p>`
  for (i = 0; i < standards.length; i++) {
    content += `<li>${standards[i]} <button onclick=delete_standard(${i})>delete</button></li>`
  }
  // content += `<input type="number" id="std" placeholder="Standard">
  // <label >Section:</label><br><input type="text" id="sec" placeholder="section">
  // <button onclick=add()>add</button>
  // <hr>`
  document.querySelector('.standard-edit').innerHTML = content
}

// profile details get function
function profile() {
  console.log(token)
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
        console.log("data=", data.data.email)
        console.log("data=", data)

        let htmlSegment = `<div class="user d-flex flex-wrap flex-column" id='${data.data.id}'>
              <div class="profile-head">
              <div class='image'> <img src='http://127.0.0.1:8000/${data.data.profile?.profile_picture}'></div>  
              <p class="fullname">${data.data.profile?.full_name}</p><br>`
        console.log(data.data.profile?.standard.length)
        if (user != 'is_student') {
          let content = ''
          content += `    <p> standards list</p>`
          standards = data.data.profile?.standard
          for (i = 0; i < standards.length; i++) {
            content += `
                    <li>${standards[i]} <button onclick=delete_standard(${i})>delete</button></li>`
          }
          // content += `<input type="number" id="std" placeholder="Standard">
          // <label >Section:</label><br><input type="text" id="sec" placeholder="section">
          // <button onclick=add()>add</button>
          // <hr>`

          document.querySelector('.standard-edit').innerHTML = content
        }
        // user type wise profile details
      
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