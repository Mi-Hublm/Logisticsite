

function changeBackgroundImage(pageName = null) {
  
  const bannerElement = document.getElementById('banner');

  // Define a mapping of page names to background images
  const backgroundImages = {
    index: '/static/Img/Photo.png',
    team: '/static/Img/photo1111.png',
    about: '/static/Img/photo2222.png',
    contact: '/static/Img/photo7777.png',
    blog: '/static/Img/photo99.png',
  };

  // Check if the pageName exists in the backgroundImages object
  if (pageName && backgroundImages.hasOwnProperty(pageName)) {
    // Set the background image of the banner element
    bannerElement.style.backgroundImage = `url(${backgroundImages[pageName]})`;
  } else {
    // If the pageName is found  default background image
    bannerElement.style.backgroundImage = 'url("/static/Img/Photo1111.png")';
  }
}


window.addEventListener("load", () => {
  const loader = document.querySelector(".loader")
  loader.classList.add("loader-hide");
  
  loader.addEventListener("transitioned", () => {
    document.body.removeChild(loader)
  })
})