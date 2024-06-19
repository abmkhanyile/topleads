$(document).ready(function() {

  $('.biz-provinces').select2({
    tags: true,
    maximumSelectionLength: parseInt($("#plan-provinces").attr("data-provinces"))
  });

  $('.biz-categories').select2({
  
  });

  $('.biz-keywords').select2({
  });

  $('.select2-search__field').autocomplete({
    source: function(request, response ){
        if(request.term.length >= 3){
            $.ajax({
                url: "/user-accounts/find-keywords/",
                type: 'POST',
                data: {
                    'search_text': request.term,
                    'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val()
                },
                success: function(data){
                  console.log(data)
                  if(data.length > 0){
                    // $('.biz-keywords').empty();
                    for(let i = 0; i < data.length; i++){
                      var newOption = new Option(data[i].fields.keyword, data[i].pk, false, false);
                      $('.biz-keywords').append(newOption).trigger('change');
                      console.log(data[i].pk)
                    };
                  }
                    
                },
                dataType: 'json'
            });
        }
        else{
            // $('.biz-keywords').empty();
            response([]);
        }
    }
});

  
});

// password show/hide toggle eye.
function hide_show_pwd(elem){
  const togglePassword = $(elem); //document.querySelector("#togglePassword");
  const password = document.querySelector("#password");

    // toggle the type attribute
    const type = password.getAttribute("type") === "password" ? "text" : "password";
    password.setAttribute("type", type);
    // toggle the eye icon
    togglePassword.toggleClass('fa-eye');
    togglePassword.toggleClass('fa-eye-slash');
  
}