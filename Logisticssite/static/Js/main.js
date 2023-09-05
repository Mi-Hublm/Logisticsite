function changeBackgroundImage(pageName = null) {
  
  const bannerElement = document.getElementById('banner');

  // Define a mapping of page names to background images
  const backgroundImages = {
    index: '/static/Img/Photo1111.png',
    team: '/static/Img/photo9.png',
    about: '/static/Img/photo7777.png',
    contact: '/static/Img/photo7777.png',
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
