// JavaScript Document
var countdown=60; 
// function settime(val) { 
// 	$(val).attr("disabled", true); 
// 	if (countdown == 0) { 
// 		$(val).attr("disabled",false); 
// 		$(val).text("获取到短信验证码"); 
// 		countdown =60; 
// 	} else { 
// 		$(val).text(countdown+"秒后可重新发送"); 
// 		countdown--; 
// 		setTimeout(function() { 
// 			if (countdown !== 0)
// 			{
// 				$(val).text(countdown+"秒后可重新发送"); 
// 				countdown--;
// 			}
			
// 		},1000) 
// 	} 

// } 
// $(function(){
//      $(".tipTimer").trigger("click");
// })
function time_change(val)
{
	if (countdown != 0)
	{
		$(val).text(countdown+"秒后可重新发送"); 
		countdown--;
		setTimeout(function() { 
			time_change(val); 
		},1000) 
	}
	else 
	{
		$(val).attr("disabled",false); 
		$(val).text("获取到短信验证码"); 
		countdown =60; 
	}
}
function settime(val)
{
	$.ajax({
		url:'/email_exam/',
		type:'post',
		data:{eamil:$('#email').val()},
		dataType:'JSON',
		success:function(data){
			
		}
	});
	$(val).attr("disabled", true); 
	$(val).text(countdown+"秒后可重新发送"); 
	countdown--;
	time_change(val);
}

var countdown1 = 5;
function time_change2(val){
	if (countdown != 0)
	{
		val.text(`注册成功,即将在${countdown1}秒后为您跳转到登录页面！`); 
		countdown1--;
		setTimeout(function() { 
			time_change2(val); 
		},1000) 
	}
	else 
	{
		countdown1 = 4; 
	}
}
function settime2(val)
{
	$(val).text(`注册成功,即将在${countdown1}秒后为您跳转到登录页面！`); 
	countdown1--;
	time_change2(val);
}