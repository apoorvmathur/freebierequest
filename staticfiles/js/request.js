var cards = 0;

var approve = function(id) {
	var user = localStorage.user;
	var token = localStorage.token;
	
	var comment_text = $('#comment-'+id).val()
	console.log("Approve: "+id+" Comment: " +comment_text)
	
	$.post("http://127.0.0.1:8000/update/", {user: user, token:token, id:id, status:"Approved", comment:comment_text}, function(data, status){
		console.log(status)
	})
	$("#card-"+id).remove()
	cards = cards - 1;
	console.log(cards)
	if(cards == 0) {
		$("#no-cards").show()
	}
	
	location.reload();
}

var reject = function(id) {
	var user = localStorage.user;
	var token = localStorage.token;
	
	var comment_text = $('#comment-'+id).val()
	
	$.post("http://127.0.0.1:8000/update/", {user: user, token:token, id:id, status:"Rejected", comment:comment_text}, function(data, status){
		console.log(status)
	})
	console.log("Reject "+id)
	$("#card-"+id).remove()
	cards = cards - 1;
	console.log(cards)
	if(cards == 0) {
		$("#no-cards").show()
	}
	
	location.reload();
}

$(document).ready(function(){
	
	if(localStorage.user == null || localStorage.token == null) {
		console.log("User Not Found!")
		window.location.replace("login.html");
	}
	
	
	var user = localStorage.user;
	var token = localStorage.token;
	
	console.log(token)
	
	$.post("http://127.0.0.1:8000/request/", {user: user, token:token}, function(data, status){
		console.log(data)
		var request_list = data["data"];
		console.log(request_list)
		cards = request_list.length;
		if(request_list.length != 0) {
			for(request in request_list) {
				curr_request = request_list[request]
				html_str = '<div class="card border-primary freebie-card custom-card m-2" id="card-'+curr_request["id"]+'">\
				<div class="card-body">\
				<p class="card-text">\
				Agent: '+curr_request["agent_name"]+'</p>\
				Category: '+curr_request["category"]+'</p>\
				User ID: '+curr_request["user_id"]+'</p>\
				Account Phone: '+curr_request["account_phone"]+'</p>\
				Sale Date: '+curr_request["sales_date"]+'</p>\
				Activation Date: '+curr_request["activation_date"]+'</p>\
				Sale Amount: '+curr_request["sales_amount"]+'</p>\
				Previous Sales: '+curr_request["prev_sales"]+'</p>\
				Discount Amount: '+curr_request["discount_amount"]+'</p>\
				Discount Percent: '+curr_request["discount_percent"]+'%</p>\
				Discussion Details: '+curr_request["discussion_details"]+'</p>\
				Status: '+curr_request["status"]+'</p>'
				if(curr_request["action"]) {
					html_str = html_str+'<a href="javascript:approve('+curr_request["id"]+')" class="btn btn-success mx-1 p-2">Approve</a>\
					<a href="javascript:reject('+curr_request["id"]+')" class="btn btn-danger mx-1 p-2">Reject</a><br>\
					<label class="col-form-label">Comment</label>\
					<textarea class="form-control" id="comment-'+curr_request["id"]+'" rows="3" placeholder="Add Comment"></textarea>'
				} else{
					if(curr_request["comment"]) {
						html_str = html_str + 'Comments: '+curr_request["comment"]+'</p>'
					} if(curr_request["updated_by"]) {
						html_str = html_str + 'Updated By: '+curr_request["updated_by"]+'</p>'
					}
				}
				html_str = html_str + '</div></div>'
				$("#request-container").append(html_str)
			}
		} else {
			$("#no-cards").show()
		}
	});
	
	$("#no-cards").hide();
	$("#logout").click(function(){
		localStorage.removeItem("user")
		localStorage.removeItem("token")
		window.location.replace("login.html");
	});
	
	console.log("Ready!")
	
});
