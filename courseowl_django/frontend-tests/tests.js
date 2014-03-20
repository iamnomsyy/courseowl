var siteUrl = 'http://127.0.0.1:8000/'; // not sure how to deal with production vs dev

casper.test.begin('Homepage works', function suite(test) {
  casper.start(siteUrl, function() {
     test.assertHttpStatus(200, 'Site is up and running');
     var signupButtonSelector = '#signup-button';
     test.assertExists(signupButtonSelector, 'Signup button present');
     this.click(signupButtonSelector);
  });

  // Clicked signup button, should be on signup page
  casper.then(function() {
    test.assert(this.getCurrentUrl() === (siteUrl + 'accounts/signup/'), 'Sign up page accessible from home page');
  });

  casper.thenOpen(siteUrl, function() {
    var signInSelector = '#signin-button';
    test.assertExists(signInSelector, 'Sign in button exists');
    this.click(signInSelector);
  });

  // Clicked sign in button
  casper.then(function() {
    test.assert(
      this.getCurrentUrl() === (siteUrl + 'accounts/login/'),
      'Login accessible from home page'
    );
  });

  casper.run(function() {
      test.done();
  });
});

casper.test.begin('Sign up process', function suite(test) {
  casper.start(siteUrl+'accounts/signup', function() {
    // TODO: find better way of testing new account creation with temp accounts
    var emailAddress = Date.now().toString() + '@test.com';
    var signupUrl = this.getCurrentUrl();

    test.assertExists('form', 'Sign up form exists');
    this.fill('form', {
      'email': '',
      'password': '',
      'password_confirm': ''
    }, true);

    test.assert(this.getCurrentUrl() === signupUrl, 'Empty submit back to signup');

  });

  casper.run(function() {
    test.done();
  });
});