document.addEventListener("DOMContentLoaded", AllPostsDisplayer());

function AllPostsDisplayer()
{
   fetch("/all-posts")
   .then(response => response.json())
   .then(posts => {
        posts.forEach(post => {
            postDiv = document.createElement("div");
            postDiv.classList.add("post");

            postDiv.innerHTML = `
                <h4><a href="profile/${post.user}">${post.user}</a></h4>
                <p>${post.post_content}</p>
                <span>${post.creation_date}</span>
                <span>Likes: ${post.likes}</span>
            `;

            // Append Div
            document.querySelector("#all-posts-container").append(postDiv);
        });
   })
}