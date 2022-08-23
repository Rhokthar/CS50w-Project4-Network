document.addEventListener("DOMContentLoaded", function() {
    // Select Buttons
    let editButtonsArray = document.querySelectorAll(".edit-btn");
    let saveButtonsArray = document.querySelectorAll(".save-edit-btn");

    for (let i = 0; i < editButtonsArray.length; i++)
    {
        // Add OnClick Event to Edit Buttons
        editButtonsArray[i].onclick = () => {
            // Hide/Visualize Post Parts
            document.querySelector(`#post-${editButtonsArray[i].value} .post-content`).style.display = "none";
            document.querySelector(`#post-${editButtonsArray[i].value} .edit-btn`).style.display = "none";
            document.querySelector(`#post-${editButtonsArray[i].value} .edit-post-text`).style.display = "block";
            document.querySelector(`#post-${editButtonsArray[i].value} .save-edit-btn`).style.display = "block";
        }
        // Add OnClick Event to Save Buttons
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
                document.querySelector(`#post-${editButtonsArray[i].value} .edit-post-text`).style.display = "none";
                document.querySelector(`#post-${editButtonsArray[i].value} .save-edit-btn`).style.display = "none";

            }, 200);
        }
    }
}); 