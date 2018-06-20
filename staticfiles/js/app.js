var alternate_numbers = 0;
var alternate_numbers_list = [];

var remove = function(index) {
	console.log(alternate_numbers_list)
	$("#alternate_phone_div_"+index).remove()
	alternate_numbers -= 1
	const i = alternate_numbers_list.indexOf('alternate_phone_div_'+index);
	if(i != -1){
		alternate_numbers_list.splice(i, 1);
	}
	console.log(alternate_numbers_list)
}

$(document).ready(function(){
	
    var sales_date_input=$('#sales_date');
	var activation_date_input=$('#activation_date');
    var container=$('.bootstrap-iso form').length>0 ? $('.bootstrap-iso form').parent() : "body";
    var options={
		format: 'yyyy-mm-dd',
		container: container,
		todayHighlight: true,
		autoclose: true,
    };
    sales_date_input.datepicker(options);
	activation_date_input.datepicker(options);
	
	console.log("Fetching agents")
	
	$.post("http://127.0.0.1:8000/agents/",{}, function(data, status) {
		agent_list = data.agents;
		console.log(agent_list)
		for(i in agent_list){
			console.log(agent_list[i])
			$("#agent_name").append('<option value="'+agent_list[i]+'">'+agent_list[i]+'</option>')
		}
	});
	
	var validate = function() {
		
		for(i in alternate_numbers_list) {
			console.log("#"+alternate_numbers_list[i])
			console.log($("#"+alternate_numbers_list[i]).val());
		}
				
		var phoneno = /^\d*$/;
		var number = /^\d*$/;
		
		var agent_name = $("#agent_name").val()
		if(agent_name == "" || agent_name == "Agent Name") {
			alert( "Please provide your name!" );
            $("#agent_name").focus() ;
            return false;
		}
		
		var category = $("#category").val()
		if(category == "" || category == "Category") {
			alert( "Please select category!" );
            $("#category").focus() ;
            return false;
		}
		
		var account_phone = $("#account_phone").val()
		if(account_phone == "" || !(account_phone.match(number))) {
			alert( "Please provide a valid phone number!" );
            $("#account_phone").focus() ;
            return false;
		}
		
		var user_id = $("#user_id").val()
		if(user_id == "" || !(user_id.match(number))) {
			alert( "Please provide a valid User ID number!" );
            $("#user_id").focus() ;
            return false;
		}
		
		var sales_date = $("#sales_date").val()
		if(sales_date == "") {
			alert( "Please provide a valid sales date!" );
            $("#sales_date").focus() ;
            return false;
		}
		
		var activation_date = $("#activation_date").val()
		if(activation_date == "") {
			alert( "Please a valid activation date!" );
            $("#activation_date").focus() ;
            return false;
		}
		
		var sales_amount = $("#sales_amount").val()
		if(sales_amount == "" || !(sales_amount.match(number))) {
			alert( "Please enter a valid sale amount!" );
            $("#sales_amount").focus() ;
            return false;
		}
		
		var previous_sales = $("#previous_sales").val()
		if(previous_sales == "" || !(previous_sales.match(number))) {
			alert( "Please enter a valid sale amount!" );
            $("#previous_sales").focus() ;
            return false;
		}
		
		var discount_amount = $("#discount_amount").val()
		if(discount_amount == "" || !(discount_amount.match(number))) {
			alert( "Please enter a valid discount amount!" );
            $("#discount_amount").focus() ;
            return false;
		}
		
		var discussion_details = $("#discussion_details").val()
		if(discussion_details == "") {
			alert( "Please enter discussion details!" );
            $("#discussion_details").focus() ;
            return false;
		}
		
		for(i = 1; i <= alternate_numbers; i++) {
			console.log("#alternate_phone_"+i)
			var alternate_phone = $("#alternate_phone_"+i).val()
			if(alternate_phone.length == "" || !(alternate_phone.match(phoneno))) {
				alert( "Please provide a valid phone number!" );
				$("#alternate_phone_"+i).focus() ;
				return false;
			}
		}
		
		return true;
	}
	
	var submit = function() {
		var agent_name = $("#agent_name").val()
		var category = $("#category").val()
		var account_phone = $("#account_phone").val()
		var user_id = $("#user_id").val()
		var sales_date = $("#sales_date").val()
		var activation_date = $("#activation_date").val()
		var sales_amount = $("#sales_amount").val()
		var previous_sales = $("#previous_sales").val()
		var discount_amount = $("#discount_amount").val()
		var discount_percent = $("#discount_percent").val()
		var discussion_details = $("#discussion_details").val()
		var alternate_numbers_list = []
		
		for(i = 1; i <= alternate_numbers; i++) {
			var alternate_phone = $("#alternate_phone_"+i).val()
			alternate_numbers_list.push(alternate_phone)
		}
		
		var alternate_numbers_string = String(alternate_numbers_list)
		
		request_param = {}
		
		request_param["agent_name"]=agent_name
		request_param["category"]=category
		request_param["account_phone"]=account_phone
		request_param["user_id"]=user_id
		request_param["sales_date"]=sales_date
		request_param["activation_date"]=activation_date
		request_param["sales_amount"]=sales_amount
		request_param["prev_sales"]=previous_sales
		request_param["discount_amount"]=discount_amount
		request_param["discount_percent"]=discount_percent
		request_param["discussion_details"]=discussion_details
		request_param["alternate_number"]=alternate_numbers_string
		request_param["status"]="Pending"
		
		$.post("http://127.0.0.1:8000/insert/", request_param, function(data, status){
			$("#success-section").show();
			$("#form-section").hide();
		})
	}
	
	$("#add-number").click(function(){
		console.log("Adding alternate number!")
		alternate_numbers = alternate_numbers + 1;
		$("#alternate-phone-div").append('<div id="alternate_phone_div_'+alternate_numbers+'"><div>\
			<label class="col-form-label" for="alternate_phone">Altername Phone '+alternate_numbers+'</label>\
			</div><a href=javascript:remove('+alternate_numbers+')>\
			<div style="display:inline-block; clear:left; margin:20px"><i class="fa fa-minus-circle ml-2"></i></div></a>\
			<input type="text" class="form-control" id="alternate_phone_'+alternate_numbers+'" placeholder="Alternate Phone" style="width:90%; float:right;">\
			</div>')
		alternate_numbers_list.push('alternate_phone_div_'+alternate_numbers)
	});
	
	$("#submit-button").click(function(e){
		valid = validate()
		if(valid){
			submit()
		}
	});
	
	$("#reset-form").click(function() {
		$("#success-section").hide();
		$("#form-section").show();
		window.location.reload(false);
	});
	
	$("#success-section").hide();
	
	$("#sales_amount").change(function(e){
		console.log("changed!")
		var sales_amount = $("#sales_amount").val()
		var discount_amount = $("#discount_amount").val()
		var discount = ((discount_amount)*100/sales_amount).toFixed(2)
		if(sales_amount != "" && discount_amount != "") {
			$("#discount_percent").val(discount)
		}
	});
	
	$("#discount_amount").change(function(e){
		console.log("changed!")
		var sales_amount = $("#sales_amount").val()
		var discount_amount = $("#discount_amount").val()
		var discount = ((discount_amount)*100/sales_amount).toFixed(2)
		if(sales_amount != "" && discount_amount != "") {
			$("#discount_percent").val(discount)
		}
	});
	
});

