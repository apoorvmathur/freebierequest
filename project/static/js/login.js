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
		console.log(password)
		
		$.post("http://127.0.0.1:8000/user/", {user: user, password:password}, function(data, status){
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