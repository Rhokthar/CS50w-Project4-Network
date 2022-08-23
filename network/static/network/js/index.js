document.addEventListener("DOMContentLoaded", function() {
    // Select Buttons
    let editButtonsArray = document.querySelectorAll(".edit-btn");
    let saveButtonsArray = document.querySelectorAll(".save-edit-btn");
    let likeButtonsArray = document.querySelectorAll(".like-btn");

    for (let i = 0; i < likeButtonsArray.length; i++)
    {
        // Add OnClick Event to Edit Buttons
        if (i < editButtonsArray.length)
        {
            editButtonsArray[i].onclick = () => {
                // Hide/Visualize Post Parts
                document.querySelector(`#post-${editButtonsArray[i].value} .post-content`).style.display = "none";
                document.querySelector(`#post-${editButtonsArray[i].value} .edit-btn`).style.display = "none";
                document.querySelector(`#post-${editButtonsArray[i].value} .like-btn`).style.display = "none";
                document.querySelector(`#post-${editButtonsArray[i].value} .edit-post-text`).style.display = "block";
                document.querySelector(`#post-${editButtonsArray[i].value} .save-edit-btn`).style.display = "block";
            }
        }

        // Add OnClick Event to Save Buttons
        if (i < saveButtonsArray.length)
        {
            saveButtonsArray[i].onclick = () => {
                // Get New Post Content Value
                let newContent = document.querySelector(`#post-${editButtonsArray[i].value} .edit-post-text`).value;
                // Update Post Content
                fetch(`/edit-post/${saveButtonsArray[i].value}`, {
                    method: "PUT",
                    body: JSON.stringify({
                        post_content: `${newContent}`
                    })
                })
                // Set New Post Content to Old Field
                setTimeout(function() {
                    fetch(`/edit-post/${saveButtonsArray[i].value}`, {
                        method: "GET",
                    })
                    .then(response => response.json())
                    .then(post => {
                        document.querySelector(`#post-${editButtonsArray[i].value} .post-content`).innerHTML = post.post_content;    
                    })

                    // Hide/Visualize Post Parts
                    document.querySelector(`#post-${editButtonsArray[i].value} .post-content`).style.display = "block";
                    document.querySelector(`#post-${editButtonsArray[i].value} .edit-btn`).style.display = "block";
                    document.querySelector(`#post-${editButtonsArray[i].value} .like-btn`).style.display = "block";
                    document.querySelector(`#post-${editButtonsArray[i].value} .edit-post-text`).style.display = "none";
                    document.querySelector(`#post-${editButtonsArray[i].value} .save-edit-btn`).style.display = "none";

                }, 200);
            }
        }

        // Add OnClick Event to Like Buttons
        likeButtonsArray[i].onclick = () => {
            console.log(likeButtonsArray[i].value);
            fetch(`/like-post/${likeButtonsArray[i].value}`, {
                method: "PUT"
            })
            // Set New Post Likes
            setTimeout(function() {
                fetch(`/like-post/${likeButtonsArray[i].value}`, {
                    method: "GET"
                })
                .then(response => response.json())
                .then(post => {
                    document.querySelector(`#post-${likeButtonsArray[i].value} .likes`).innerHTML = `Likes: ${post.likes}`
                    
                    let buttonWord = document.querySelector(`#post-${likeButtonsArray[i].value} .like-btn`);
                    if (buttonWord.innerHTML === "Like")
                    {
                        buttonWord.innerHTML = "Unlike";
                    } else {
                        buttonWord.innerHTML = "Like";
                    }
                })
            }, 200);
        }
    }
}); 