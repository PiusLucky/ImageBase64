"Conveniently convert png, jpg, webp and gif to base64 string - Encode
and also, convert your base64 string in any format to Image - Decode"


## 🚀 Features:
<ol>
	<li>File formats accepted include jpeg, png, gif, and webp</li>
	<li>Encoding of all file formats listed above</li>
	<li>Decoding of Base64 string with contents that possess the above four formats</li>
	<li>Downloading of Base64 string compiled in a text format </li>
	<li>Downloading of converted image file is enabled</li>
	<li>Active quick preview of uploads in real time</li>
	<li>Tracking of the user's browser for experimental purposes</li>
    <li> Full View of encoded image</li>
	<li>Contact Tab</li>
	<li>Update Tab</li>
	<li>Encode Image from any direct image link (Advance)
	<li>Integreted Application Programming Interface (API) <code style="color: green">new</code></li>

</ol>

## 🚀 New Release:  ImageBase64 API -  v1.0.1 
https://image2base64.herokuapp.com/api/doc/<br>
A Web API for encoding image to Base64 string and decoding any base64 string back to image.<br>

### Instructions to registering for the ImageBase64 Integrated API
https://image2base64.herokuapp.com/api/doc/<br>
1. Click on the api endpoint [POST] /v1/rest-auth/registration/<br>
2. Click on the "Try it Out" button <br>
3. Enter your details <br>
4. Click on the "Execute" button<br>
5. Then copy & paste the generated key into the endpoint [POST] /v1/rest-auth/registration/verify-email/<br>
6. Ignore the csrf_token error (It is an expected error)<br>
7. Go to the top and click the "Login" button';<br>


### Guide on consuming ImageBase64API via the terminal (Using the requests library)
### Python Case
First install requests library <br>
```python
pip install requests
```
Then, run the following lines of code:

```python
import requests
context = {"username": "userabc", "email": "userabc@gmail.com", "password": "userabc12345" }  
r = requests.post('https://image2base64.herokuapp.com/api/v1/rest-auth/login/', data = context)  
print(r.text) 

url = {"url": "https://image2base64.herokuapp.com/media/photo-1511469054436-c7dedf24c66b.jpg"}

encode_link = requests.post("https://image2base64.herokuapp.com/api/v1/link/encode/", data = url, headers={ 'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTgyNzI2Nzk0LCJqdGkiOiI1YzBiNjY5ODIxNWY0ZjNiYmU4ODhjOWZlMzBjMjYxNCIsInVzZXJfaWQiOjN9.84hv-O12BvcIjOyESelPT9-ReoAna3w4505BWu9HHrc' }) 

print(r) 
print(r.text) 
print(encode_link) 
output_dict = encode_link.json() 
print(output_dict["image_info"])

```

### Using Javascript:
Use the link below for the corresponding HTML for the javascript snippet<br>
<code><a href="https://github.com/PiusLucky/ImageBase64/blob/master/ConsumeAPI%20Test/APP/javascript/index.html">https://github.com/PiusLucky/ImageBase64/blob/master/ConsumeAPI%20Test/APP/javascript/index.html</a></code>
<br>
```javascript
$.ajax({
method: "POST",
url: 'https://image2base64.herokuapp.com/api/v1/rest-auth/login/',  //the url to call
data: {
	"username": "userabc12345",
	"email": "userabc12345@gmail.com",
	"password": "userabc12345"
}, 

headers: {
	"Accept": "application/json",
},

dataType: "json",

success: function (x) {
	const login_key = document.querySelector("#login_key")
	login_key.append(x["key"])    
}

});

// NB: valid link must include "www"
var link = 'https://www.sample-videos.com/img/Sample-jpg-image-50kb.jpg' 
$.ajax({
	method: "POST",
	url: 'https://image2base64.herokuapp.com/api/v1/link/encode/',  //the url to call
	data: JSON.stringify({
	"url": link,
	"username": "userabc12345",
	"email": "userabc12345@gmail.com",
	"password": "userabc12345"
}), 
	headers: {
		"Accept": "application/json",
		"Content-Type":"application/json",
	},
	contentType: "application/json",
	dataType: "json",

	success: function (response) {
		const encode_info = document.querySelector("#encode_info")
		const encode_id = document.querySelector("#encode_id")
		const image_size = document.querySelector("#image_size")
		const image_extension = document.querySelector("#image_extension")
		const image_name = document.querySelector("#image_name")
		const image_dimension = document.querySelector("#image_dimension")
		encode_id.append(response["encode_id"])
		image_size.append(response["image_info"]["image_size"])
		image_extension.append(response["image_info"]["image_extension"])
		image_name.append(response["image_info"]["image_name"])
		image_dimension.append(response["image_info"]["image_dimension"])
		encode_info.append(response["raw_copy_base64"])
	},
	error: function(response){
	const encode_info = document.querySelector("#encode_info")
	result = JSON.stringify(response)
	encode_info.append(result)
	}
	});

```


## 🚀 FAQ

<div> <b>  <code style="color: green">What is Base64?</code></b></div>
<br>
<div style="text-align: justify;">According to <a href="https://www.techopedia.com/definition/27209/base64" target="_blank">techopedia.com</a>, Base64 is an encoding and decoding technique used to convert binary data to an American Standard for Information Interchange (ASCII) text format, and vice versa. It is used to transfer data over a medium that only supports ASCII formats, such as email messages on Multipurpose Internet Mail Extension (MIME) and Extensible Markup Language (XML) data. Base64 is also known as Base64 Content-Transfer-Encoding.<br>
It is worthy of note that some tools used in rendering HTML into PDF requires an image file first be converted to Base64 before it can be rendered. 
</div>


<div> <b>  <code style="color: green">Is base64 URL safe?</code></b></div>
<br>
<div style="text-align: justify;">By consisting only in ASCII characters, base64 strings are generally url-safe, and that's why they can be used to encode data in Data URLs.</div>

<div> <b>  <code style="color: green">Can the encoded Base64 string be compiled in a text file?</code></b></div>
<br>
<div style="text-align: justify;">Yes!, the encoded base64 string is usually compiled in a text file (i.e .txt file) or can be copied directly by hitting the copy icon located at the right-hand side of the encoded output box. Meanwhile, the text file can be downloaded freely by hitting the download button.</div>


<div> <b>  <code style="color: green">why is 1.00 MB the maximum allowed for file upload?</code></b></div>
<br>
<div style="text-align: justify;">The main reason for this is that the service rendered by ImageBase64 is free and hosted on a private server, and as such we try as much as possible to keep the total uploads as small in size as possible. Though, you can always <a href="https://image2base64.herokuapp.com/contact"> contact me</a> if you intend on encoding an image with a far larger size.</div>
<div> <b>  <code style="color: green">Are uploaded files saved permanently? </code></b></div>
<br>
<div style="text-align: justify;">
Here's a graphical representation of activities behind the scene:
<br>
<br>
<div style="background-color:whitesmoke;width: 510px;max-width: 100%; max-height: auto;">
	<img src="https://image2base64.herokuapp.com/static/front-end/front_end/assets/images/schema.svg" width="50%" alt="">
</div>
<br>
The explanations go thus:
<ul>
	<li>The image is uploaded to a specific folder depending on process.</li>
	<li>The image data is read and encoded to a base64 string.</li>
	<li>The image metadata, like size and mimetype, is read.</li>
	<li>The image is then deleted.</li>
</ul>
</div>

<div> <b>  <code style="color: green">Take a look at the background processess:</code></b></div>


<div style="background-color:whitesmoke;width: 510px;max-width: 100%; max-height: auto;">
	<img src="https://image2base64.herokuapp.com/static/front-end/front_end/assets/images/prorotype_imagebase64_svg.jpg" width="50%" alt="">
</div>



<div> <b>  <code style="color: green">How can I save the decoded Base64 string (i.e result)?</code></b></div>
<br>
<div style="text-align: justify;">Yes!, all you got to do is click on the BLUE button circled by the red rectangle in the screenshot below:
<br>
<br>
<div style="background-color:whitesmoke;width: 510px;max-width: 100%; max-height: auto;">
<img src="https://image2base64.herokuapp.com/static/front-end/front_end/assets/images/Screenshot.svg" alt="">
</div>

</div>

<p align="right"><b> Made with &#x2764; by Pius Lucky </b></p>

