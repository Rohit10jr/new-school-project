
function signup() {
    console.log('signup called')
    // // console.log(($("#signupbox").valid())) 
    // document.getElementById("myForm").submit();
    let csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    var email = document.getElementById('id_email').value
    var phone = document.getElementById('id_phone').value
    var dob = document.getElementById('id_date_of_birth').value
    var type = document.getElementById('id_user_type').value
    var firstname = document.getElementById('id_first_name').value
    var lastname = document.getElementById('id_last_name').value
    var fullname = document.getElementById('id_full_name').value
    var address = document.getElementById('id_address').value
    var is_dataentry = document.getElementById('id_data_entry_user').value
    // let details = {'email':email,'phone':phone,'dob':dob,'reg':reg,'firstname':firstname,'fullname':fullname,'address':address} 
    let signup_errors = document.querySelector('.signup-error')
    let error_content = ''
    if(!email){
        error_content += `<li class='text-danger'>email is requied</li>`
    }        
    if(!phone){
        error_content += `<li class='text-danger'>phone number is required</li>`
    }
    if(!dob){
        error_content += `<li class='text-danger'>dob is requied</li>`
    }
    if(!firstname){
        error_content += `<li class='text-danger'>firstname is requied</li>`
    }
    if(!fullname){
        error_content += `<li class='text-danger'>full name is requied</li>`
    }
    if(!address){
        error_content += `<li class='text-danger'>address is requied</li>`
    }
    if(!email || !phone || !dob || !firstname || !fullname || !address){
        $('#messageModal-signup').modal('show')
        signup_errors.innerHTML = error_content
        return
    }

    /*var email = 's@gmail.com'
    var phone =  9992945428
    var dob = '2000-02-10'
    var reg ='s10'
    var standard = 1
    var section = 'c'
    var type = 'is_student'
    var firstname = 's'
    var lastname = 'p'
    var fullname = 'sp'
    var address ='home'
    var is_dataentry = 'false'*/
    if(document.getElementById('id_standard')){
    standard = document.getElementById('id_standard').value
    section = document.getElementById('id_section').value
    }
    if (!standards.length && standard && section) {
        standards.push(standard + '-' + section)
    }else if(type=='is_student'){
        document.querySelector('.signup-errors').innerHTML = '<li class="text-center text-danger">add a standard and section</li>'
        return
    }
    fetch('http://127.0.0.1:8000/api/signup/',
        {
            method: 'POST',
            body: JSON.stringify({
                'email': email, 'phone': phone, 'date_of_birth': dob, 'user_type': type,
                'is_data_entry': is_dataentry, 'first_name': firstname, 'last_name': lastname, 'standard': standards, 'full_name': fullname, 'address': address
            }
            ),
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
        }).then(res => {
            return res.json()
        }).then(data => {
            if (`${data.status}` == 'Registered succesfull') {
                window.location.href = `${host}/login`
            }
            document.getElementById('response').innerHTML = `${data.data.error[0]}`
            document.getElementById('response').style.display = 'block'
        })
    return true;
}




let input = document.getElementById('id_address')
input.addEventListener('keyup', (e) => {
    if (e.keyCode === 13) {
        signup();
    }
})



function check_email(element){
    console.log(element.value)
    url_for_check = new URL('http://127.0.0.1:8000/api/check-user/');
    url_for_check.searchParams.append('email', element.value);
    fetch(url_for_check, {
        method: 'GET',
    }).then(res => {
        console.log(res,res.status)
        if(res.status != 200){
            document.querySelector('.email-error').innerHTML = 'email altready exits' 
        }
        else{
            document.querySelector('.email-error').innerHTML = ''
        }
    })
}
function check_phone(element){
    url_for_check = new URL('http://127.0.0.1:8000/api/check-user/');
    url_for_check.searchParams.append('phone', element.value);
    fetch(url_for_check, {
        method: 'GET',
    }).then(res => {
        if(res.status != 200){
            document.querySelector('.phone-error').innerHTML = 'phone number altready exits' 
        }else{
            document.querySelector('.phone-error').innerHTML = ''
        }
    })
}