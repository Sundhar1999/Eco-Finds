document.addEventListener('DOMContentLoaded', () => {
    showSection('dashboard'); // Show dashboard by default

    const accountForm = document.getElementById('account-details-form');
    if (accountForm) {
        accountForm.addEventListener('submit', function(event) {
            event.preventDefault();
            saveAccountDetails();
        });
    }
});

function showSection(sectionId) {
    const sections = document.querySelectorAll('.content-section');
    sections.forEach(section => {
        section.classList.remove('active');
    });
    document.getElementById(sectionId).classList.add('active');
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function logout() {
    const csrftoken = getCookie('csrftoken');
    console.log("CSRF Token:", csrftoken);

    fetch("{% url 'logout' %}", {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/json',
        },
        credentials: 'same-origin'
    }).then(response => {
        if (response.ok) {
            console.log('Logout successful');
            window.location.href = '/';
        } else {
            console.error('Logout failed', response.statusText);
            alert('Logout failed.');
        }
    }).catch(error => {
        console.error('Error:', error);
    });
}

function editAccountDetails() {
    document.getElementById('account-details-static').style.display = 'none';
    document.getElementById('account-details-form').style.display = 'block';
}

function cancelEdit() {
    document.getElementById('account-details-form').style.display = 'none';
    document.getElementById('account-details-static').style.display = 'block';
}

function saveAccountDetails() {
    document.getElementById('account-details-form').style.display = 'none';
    document.getElementById('account-details-static').style.display = 'block';
}

function setUserDetails(username, bio, profilePictureUrl) {
    document.getElementById('username').textContent = username;
    document.getElementById('user-bio').textContent = bio;
    document.getElementById('profile-picture').src = profilePictureUrl;

    document.getElementById('detail-username').textContent = username;
    document.getElementById('detail-email').textContent = username.toLowerCase() + '@example.com';
    document.getElementById('detail-phone').textContent = '123-456-7890';
}
