const bar = document.getElementById("bar")
const ul = document.getElementById("ul")

bar.addEventListener("click", ()=>{
    ul.classList.toggle("h-0")
    ul.classList.toggle("h-[14rem]")
    bar.classList.toggle("rotate-90")
})