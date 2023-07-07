const likeCount = document.getElementById("likecount");
const likeIcon = document.getElementById("likeicon");

likeIcon.onclick = () => {
    const blogId = likeIcon.getAttribute("data-blog");
    const url = `/blog_like/${parseInt(blogId)}/`;

    fetch(url, {
        method: "GET",
        headers: {
            "Content-type": "application/json; charset=UTF-8",
        }
    }).then((response) => {
        return response.json();
    }).then((data) => {
        if(data.liked) {
            likeIcon.classList.remove("empty-heart");
        }else {
            likeIcon.classList.add("empty-heart");
        }
        likeCount.innerHTML = data.like_count;
    }).catch((error) => {
        console.log(error);
    })
}
