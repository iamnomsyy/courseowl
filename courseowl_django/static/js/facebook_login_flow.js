// Facebook login
window.fbAsyncInit = function() {
  FB.init({
    appId      : '218782404991692', // Courseowl appID
    status     : true, // check login status
    cookie     : true, // enable cookies to allow the server to access the session
    xfbml      : false  // Performance waste
  });

  FB.Event.subscribe('auth.login', function(resp) {
    window.location = '/facebook_login_flow';
  });
};

FB.event.subscribe('auth.authResponseChange', function(response) {
  if (response.status === 'connected') {

  } else if (response.status === 'not_authorized') {
    FB.login();
  } else {
    FB.login();
  }
});

// Load the SDK asynchronously
(function(d, s, id) {
  var js, fjs = d.getElementsByTagName(s)[0];
  if (d.getElementById(id)) return;
  js = d.createElement(s); js.id = id;
  js.src = "//connect.facebook.net/en_US/all.js#xfbml=1&appId=218782404991692";
  fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));