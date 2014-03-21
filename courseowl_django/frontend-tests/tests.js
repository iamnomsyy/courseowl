var siteUrl = 'http://www.courseowl.com/'; // not sure how to deal with production vs dev

casper.test.begin('Homepage works', function suite(test) {
  casper.start(siteUrl, function() {
     test.assertHttpStatus(200, 'Site is up and running');
     var signupButtonSelector = '#signup-button';
     test.assertExists(signupButtonSelector, 'Signup button present');
     this.click(signupButtonSelector);
  });

  // Clicked signup button, should be on signup page
  casper.then(function() {
    test.assertEquals(
      this.getCurrentUrl(),
      (siteUrl + 'accounts/signup/'),
      'Sign up page accessible from home page'
    );
  });

  casper.thenOpen(siteUrl, function() {
    var signInSelector = '#signin-button';
    test.assertExists(signInSelector, 'Sign in button exists');
    this.click(signInSelector);
  });

  // Clicked sign in button
  casper.then(function() {
    test.assertEquals(
      this.getCurrentUrl(),
      (siteUrl + 'accounts/login/'),
      'Login accessible from home page'
    );
  });

  casper.run(function() {
      test.done();
  });
});

casper.test.begin('Sign up process', function suite(test) {
  // TODO: find better way of testing new account creation by using temp accounts
  var emailAddress = Date.now().toString() + '@t.co';
  var password = 'password';
  var signupUrl = siteUrl + 'accounts/signup';
  var serverSideInvalid = 'div.alert';

  casper.start(signupUrl, function() {
    test.assertExists('form', 'Sign up form exists');
    // Attempt to submit empty form
    this.fill('form', {}, true);

    test.assertEquals(
      this.getCurrentUrl(),
      signupUrl,
      'Empty submit back to signup'
    );
    test.assertDoesntExist(serverSideInvalid, 'No request on empty form submit');

    // Attempt to sign up with no password
    var formData = {'email': emailAddress};
    this.fill('form', formData, true);

    test.assertEquals(
      this.getCurrentUrl(),
      signupUrl,
      'No password keeps user at sign up page'
    );
    test.assertEquals(
      this.evaluate(function() {
        return __utils__.getFieldValue('email');
      }),
      formData.email,
      'Email retained when other values not present'
    );
    // Make sure that there is no server side validation for empty fields
    test.assertDoesntExist(serverSideInvalid, 'No server request for missing password');

    this.fill('form', {'password': password}, true);
    test.assertDoesntExist(serverSideInvalid, 'No server request for missing confirm password');

    // invalid email
    this.fill('form', {
      'email': 'stuff',
      'password': password,
      'password_confirm': password
    }, true);
  });

  // invalid email form submitted
  casper.then(function() {
    test.assertEquals(
      this.getCurrentUrl(),
      signupUrl,
      'Invalid email returns user to sign up page'
    );
    // TODO fickle test
    //test.assertExists(serverSideInvalid, 'Email warning message displayed');

    // Clean up warning message
    //this.click('button.close');

    // invalid passwords
    this.fill('form', {
      'email': 'aslkf@tsadf.com',
      'password': password,
      'password_confirm': 'lsakdjfl'
    }, true);
  });

  // invalid password form submitted
  casper.then(function() {
    test.assertEquals(
      this.getCurrentUrl(),
      signupUrl,
      'Non matching passwords returns user to sign up page'
    );
    // TODO fickle test
    // test.assertExists(serverSideInvalid, 'Password warning message displayed');
    //this.click('button.close');

    // Correct credentials to check next part of signup flow
    this.fill('form', {
      'email': emailAddress,
      'password': password,
      'password_confirm': password
    }, true);
  });

  // We get to the personalization part of the sign up flow
  casper.then(function() {
    // For some reason casper doesn't wait for the page to load
    this.wait(500, function() {
      test.assertEquals(
        this.getCurrentUrl(),
        siteUrl + 'subject_preferences',
        'The signup was successful and user is at personalization page'
      );
      test.assertExists('.liked-subjects', 'Selected subject list exists');
      test.assertDoesntExist('.liked-subjects .list-group-item', 'By default, no selected subjects');
      test.assertExists('.other-subjects', 'All subjects list exists');
      var numSubjects = this.evaluate(function() {
        return __utils__.findAll('.other-subjects .list-group-item').length;
      });
      test.assert(numSubjects > 0, 'There exist subjects to choose from');
      this.click('.other-subjects .list-group-item:first-child');

      // The subject fades out upon removal, we have to wait for it
      this.wait(500, function() {
        test.assertExists('.liked-subjects .list-group-item', 'Subject is liked');
        var numOtherSubjects = this.evaluate(function() {
          return __utils__.findAll('.other-subjects .list-group-item').length;
        });
        test.assert(numOtherSubjects < numSubjects, 'Subject removed from unliked subjects');

        this.click('#submit-subjects');
      });
    });
  });

  casper.then(function() {
    // Wait for course preferences page to load
    this.wait(500, function() {
      test.assertEquals(
        this.getCurrentUrl(),
        siteUrl + 'course_preferences',
        'We moved from subject preferences to course preferences'
      );

      test.assertExists('.enrolled-courses', 'Enrolled course list exists');
      test.assertDoesntExist('.enrolled-courses .list-group-item', 'No course enrolled in by default');
      test.assertExists('.other-courses', 'Course list available');
      var origNumCourses = this.evaluate(function() {
        return __utils__.findAll('.other-courses .list-group-item').length;
      });
      test.assert(origNumCourses > 0, 'There are courses to choose from');
      this.click('.other-courses .list-group-item:first-child');

      // wait for fade out
      this.wait(500, function() {
        test.assertExists('.enrolled-courses .list-group-item', 'A course is enrolled in');
        var currNumCourses = this.evaluate(function() {
          return __utils__.findAll('.other-course .list-group-item').length;
        });
        test.assert(currNumCourses < origNumCourses, 'The course was removed from all courses list');

        this.click('#submit-courses');
      })

    });
  });

  casper.then(function() {
    this.wait(500, function() {
      test.assertEquals(
        this.getCurrentUrl(),
        siteUrl + 'accounts/profile',
        'Sign up flow completed'
      );
    });
  });

  casper.run(function() {
    test.done();
  });
});