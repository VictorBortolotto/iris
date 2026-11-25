function showSnackbar(message, type) {
  let scnackbar = document.getElementById("snackbar");

  scnackbar.className = "show";
  if (type === 'error') {
    scnackbar.style.backgroundColor = 'rgb(211, 65, 65)'
  } else if (type === 'alert'){
    scnackbar.style.backgroundColor = 'orange'
  } else {
    scnackbar.style.backgroundColor = 'rgb(42, 151, 42)'
  }

  scnackbar.innerText = message

  setTimeout(function(){ scnackbar.className = scnackbar.className.replace("show", ""); }, 3000);
}