var siteUrl = 'http://127.0.0.1:8000/'; // not sure how to deal with production vs dev

casper.test.begin('Homepage works', function suite(test) {
  casper.start(siteUrl, function() {
     test.assertHttpStatus(200, 'Site is up and running');
     var signupButtonSelector = 'a[href="/accounts/signup/"]';
     test.assertExists(signupButtonSelector, 'Signup button present');
     this.click(signupButtonSelector);
  });

  // Clicked signup button, should be on signup page
  casper.then(function() {
    test.assert(this.getCurrentUrl() === (siteUrl + 'accounts/signup/'), 'Sign up page accessible from home page');
  });

  casper.thenOpen(siteUrl, function() {
    var signInSelector = 'a[href="/accounts/login/"]';
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