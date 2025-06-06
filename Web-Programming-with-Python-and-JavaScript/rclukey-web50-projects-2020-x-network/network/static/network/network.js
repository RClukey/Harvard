document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll(".save_edit").forEach(div => {
        console.log(div)
    });

    document.querySelectorAll(".save_edit").forEach(form => {
        form.style.display = 'none';
    });
})

function liked(id) {
    console.log(id);
    console.log("False");

    const like_btn = document.getElementById(`like_btn_${id}`);
    const like_count = document.getElementById(`like_count_${id}`);

    if (like_btn.innerHTML === "Like") {
        fetch(`/like/${id}`)
        .then(response => response.json())
        .then(data => {
            console.log(data.message);
            console.log(like_count.innerHTML);

            like_btn.innerHTML = "Unlike";
            like_count.innerHTML = Number(like_count.innerHTML) + 1;
        });
    } else {
        fetch(`/unlike/${id}`)
        .then(response => response.json())
        .then(data => {
            console.log(data.message);
            console.log(like_count.innerHTML);

            like_btn.innerHTML = "Like";
            like_count.innerHTML = Number(like_count.innerHTML) - 1;
        });
    }
}

function edit(id) {
    console.log(id);

    document.getElementById(`edit_post_div_${id}`).style.display = "block";
    document.getElementById(`edit_post_button_${id}`).style.display = "none";
    document.getElementById(`message_${id}`).style.display = "none";
}

function edit_post(id) {
    console.log(id);

    const new_message = document.getElementById(`edit_post_${id}`).value;

    fetch(`/edit/${id}`, {
        method: "POST",
        headers: {"Content-type": "application/json", "X-CSRFToken": getCookie("csrftoken")},
        body: JSON.stringify({
            message: new_message
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
    })

    document.getElementById(`message_${id}`).innerHTML = new_message;

    document.getElementById(`edit_post_div_${id}`).style.display = "none";
    document.getElementById(`edit_post_button_${id}`).style.display = "block";
    document.getElementById(`message_${id}`).style.display = "block";
}

function getCookie(name){
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length == 2) {
        return parts.pop().split(';').shift();
    }
}