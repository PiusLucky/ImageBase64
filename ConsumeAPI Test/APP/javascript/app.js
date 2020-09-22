// One unique way of debugging the code in chrome is by using:
// 1. Network > XHR > reload the page > Name ( click on the link )
// 2. Keep an eye on the Preview Tab ( for live view of the server error).
// 3. Keep an eye on the Response Tab ( for live view of the response from server).


// This will return the login key
$.ajax({
method: "POST",
url: 'https://imagebase64.herokuapp.com/api/v1/rest-auth/login/',  //the url to call
data: {
	"username": "userabc",
	"email": "userabc@gmail.com",
	"password": "userabc12345"
}, 
// jwt: "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTgyNzI5NTMxLCJqdGkiOiIzMWRmNDZlNTFhMzg0OWFlYWUzMmFhYjc0YWY4NmZlZSIsInVzZXJfaWQiOjN9.yy9_Wlg77S5eMYWU-B3_hHAUz6dsdeMkAbabdHd93Uw",           
headers: {
	"Accept": "application/json",
	// "Authorization": "Bearer " + jwt,
},
dataType: "json",

success: function (x) {
	const login_key = document.getElementById("login_key")
	login_key.append(x["key"])

    
}

});


// NB: valid link must include "www"
var link = 'https://www.sample-videos.com/img/Sample-jpg-image-50kb.jpg' 
// jwt = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTgyNzM4MjY2LCJqdGkiOiIwYmQ3NTJjOGVmYWU0Y2I2ODQzNTJhZmU2ZTU4ZTNmYSIsInVzZXJfaWQiOjN9.lNf3CffykS7J00khBFoNy83g7haWp6IdHiNxgIm0YUU"
$.ajax({
	method: "POST",
	url: 'http://localhost:8000/api/v1/link/encode/',  //the url to call
	data: JSON.stringify({
	"url": link,
	"username": "userabc",
	"email": "userabc@gmail.com",
	"password": "userabc12345"
}), 
	headers: {
		"Accept": "application/json",
		"Content-Type":"application/json",
		// "Authorization": "Bearer " + jwt,
	},
	contentType: "application/json",
	dataType: "json",

	success: function (response) {
		const encode_info = document.getElementById("encode_info")
		const encode_id = document.getElementById("encode_id")
		const image_size = document.getElementById("image_size")
		const image_extension = document.getElementById("image_extension")
		const image_name = document.getElementById("image_name")
		const image_dimension = document.getElementById("image_dimension")

		encode_id.append(response["encode_id"])
		image_size.append(response["image_info"]["image_size"])
		image_extension.append(response["image_info"]["image_extension"])
		image_name.append(response["image_info"]["image_name"])
		image_dimension.append(response["image_info"]["image_dimension"])
		encode_info.append(response["raw_copy_base64"])

	},
	error: function(response){
	const encode_info = document.getElementById("encode_info")
	// encode_info.append(JSON.stringify(response))
	result = JSON.stringify(response)
	encode_info.append(result)
	//This shows all like so:
	// {"readyState":4,"responseText":"{\"title\":\"Link Detail\",\"name\":\"img2Base64.io\",
	// \"error_message\":\"Network Error: The link could not be accessed.
	//  Try again!\"}","responseJSON":{"title":"Link Detail","name":"img2Base64.io",
	//  "error_message":"Network Error: The link could not be accessed. Try again!"},"status":400,"statusText":"Bad Request"}
	}
	});