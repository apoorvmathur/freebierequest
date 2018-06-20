$(document).ready(function(){
	
	if(localStorage.user != null && localStorage.token != null) {
		window.location.replace("request.html");
	}
	
	$("#invalid-alert").hide()
	
	$("#submit-button").click(function(e){
		
		$("#invalid-alert").hide()
		e.preventDefault();
		
		user=$("#login").val()
		console.log(user)
		
		password=$("#password", $("#login-form")).val()
		pass = $.sha1(password)
		console.log(pass)
		
		$.post("http://192.168.133.169:8000/user/", {user: user, password:pass}, function(data, status){
			console.log(data)
			
			if(data["auth"]) {
				console.log("Success!")
				token = data["token"]
				
				localStorage["user"] = user;
				localStorage["token"] = token;
				
				window.location.replace("pending.html");
			} else {
				$("#invalid-alert").show()
			}
			
		});
	});
});
