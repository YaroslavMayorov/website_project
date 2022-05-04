let header = document.querySelector(".header");
let closeBtn = document.querySelector(".hamburger-menu");
let navBtn = document.querySelector(".nav-list");

window.addEventListener('scroll', ()=> {
    let windowPosition = window.scrollY > 0;
    header.classList.toggle('active', windowPosition)
})

       closeBtn.addEventListener("click", ()=>{
       header.classList.toggle("menu-open");
})
       navBtn.addEventListener("click", ()=>{
       header.classList.toggle("menu-open");
});
