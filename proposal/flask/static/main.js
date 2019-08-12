function navFunction(nav_id) {
    var x = document.getElementById(nav_id);
    if (x.className === "topnav") {
        x.className += " responsive";
    } else {
        x.className = "topnav";
    }
}