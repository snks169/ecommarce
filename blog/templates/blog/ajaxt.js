console.log('ajax tutorial in one video')

let fetchBtn = document.getElementById('fetchBtn')
fetchBtn.addEventListener('click', buttonClickHandler)

function buttonClickHandler(){
	console.log('fatchBtn')

	const xhr = new XMLHttpRequest();
	//open the object
	xhr.open('GET','hrry.txt',true);
	//      (type of request, 'source', synchronice or asynchronics)

	// what to do on e progress
	xhr.onprogress = function(){
		console.log('On progress');
	}
	xhr.onload =function(){
		console.log('this.responseText');
	}
	//send
	xhr.send();
}