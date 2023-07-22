
if (localStorage.getItem('mode') == null) localStorage.setItem('mode','light'); // assume light mode for new users
if (localStorage.getItem('mode') == 'dark' & document.body.classList.contains("light-mode")) toggleLightDarkMode(); // apply "preferred" dark mode over the default light mode

function toggleLightDarkMode() {
	// get the body element
	const body = document.body;
	const isLightMode = body.classList.contains("light-mode");
	if (isLightMode) localStorage.setItem('mode','dark');
	else localStorage.setItem('mode','light')
	const iconClass = isLightMode ? "bx bx-sun dark-btn" : "bx bx-moon dark-btn";
	const elementClass = isLightMode ? "dark-modalName" : "light-modalName";
	document.getElementById("icon1").className = iconClass;
	body.classList.toggle("light-mode");
	body.classList.toggle("dark-mode");
	document.querySelector("#element").classList.remove("light-modalName", "dark-modalName");
	element.classList.add(elementClass);
}

