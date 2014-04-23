var siteUrl = casper.cli.get('url'); // not sure how to deal with production vs dev, TODO use Node env variables
//console.log(siteUrl);
var timeoutTime = 3000;

function navigationTest(test, url, assertionName) {
  casper.waitForUrl(
    url,
    function then() {
      test.pass(assertionName);
    },
    function timeout() {
      test.fail(assertionName);
    }, timeoutTime
  );
}

var emailAddress = Date.now().toString() + '@t.co';
var password = 'password';

casper.test.begin('Homepage works', function suite(test) {
  var navTest = navigationTest.bind(this, test);
  casper.start(siteUrl, function() {
     test.assertHttpStatus(200, 'Site is up and running');
     var signupButtonSelector = '#signup-button';
     test.assertExists(signupButtonSelector, 'Signup button present');
     this.click(signupButtonSelector);
  });

  navTest(
    siteUrl + 'accounts/signup/',
    'Signup page accessible from home page'
  );

  casper.thenOpen(siteUrl, function() {
    var signInSelector = '#signin-button';
    test.assertExists(signInSelector, 'Sign in button exists');
    this.click(signInSelector);
  });

  navTest(
    siteUrl + 'accounts/login/',
    'Login accessible from home page'
  );

  casper.run(function() {
      test.done();
  });
});

casper.test.begin('Sign up process', function suite(test) {
  // TODO: find better way of testing new account creation by using temp accounts
  var signupUrl = siteUrl + 'accounts/signup';
  var serverSideInvalid = 'div.alert';
  var navTest = navigationTest.bind(this, test);

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

    // Correct credentials to check next part of signup flow
    this.fill('form', {
      'email': emailAddress,
      'password': password,
      'password_confirm': password
    }, true);
  });

  navTest(
    siteUrl + 'subject_preferences',
    'Signup succesful and reached subject preferences'
  );

  casper.then(function() {
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

  navTest(
    siteUrl + 'course_preferences',
    'Advanced from subject preferences to course preferences'
  );

  casper.then(function() {
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
    });
  });
// TODO check that submitted are the same as backend's courses/subjects

  navTest(
    siteUrl + 'accounts/profile',
    'Signup flow completed'
  );

  casper.run(function() {
    test.done();
  });
});

casper.test.begin('Profile page functional', function suite(test) {
  var navTest = navigationTest.bind(this, test);
  casper.start(siteUrl, function() {
    test.assertExists('#signout-button', 'Authenticated user has option to signout on homepage');
    test.assertExists('#profile-button', 'Authenticated user can navigate to profile from home page');
    this.click('#profile-button');
  });

  navTest(
    siteUrl + 'accounts/profile',
    'Authenticated user reached profile page from home page'
  );

  casper.then(function() {
    // Check that user is enrolled in one course
    test.assertExists('.enrolled-courses', 'User can see a table of enrolled courses');
    test.assertElementCount('.enrolled-courses tr', 1, 'This user is enrolled in the one course from their signup flow');

    // Check that user can choose from recommended courses
    test.assertExists('.recommended-courses', 'Recommended course table exists');
    test.assertExists('.recommended-courses tr', 'There exist recommended courses');

    test.assertExists('div .add-course', 'Add course button exists');
    this.click('.add-course');
    this.wait(5000, function() {
      test.assertElementCount('.enrolled-courses tr', 2, 'User successfully added recommended course');

      // Now we click drop course and cancel
      test.assertNotVisible('#dropCourse', 'Drop course modal is not visible');
      this.click('.drop-button');
      casper.waitUntilVisible('#dropCourse',
        function() {
          this.click('.cancel-drop-course');
          casper.waitWhileVisible('#dropCourse',
            function() {
              test.assertElementCount('.enrolled-courses tr', 2, 'No course removed on cancel');

              // this.click('.drop-button');
              // casper.waitUntilVisible('#dropCourse',
              //   function() {
              //     this.click('#confirmDrop');
              //     casper.waitWhileVisible('#dropCourse',
              //       function() {
              //         test.assertElementCount('.enrolled-courses tr', 1, 'Course was successfully dropped');
              //     });
              // });
          },
          function() {
            test.fail('Drop course modal doesn\'t disappear on cancellation');
          });
        },
        function() {
          test.fail('Drop course modal doesn\'t become visible');
      });
    });
  });

  casper.run(function() {
    test.done();
  });
});

casper.test.begin('Deleting account', function suite(test) {
  casper.start(siteUrl + 'accounts/profile', function() {
    this.click('.deactivate-button');
    casper.waitUntilVisible('#deactivate-account', function() {
      this.click('#confirmDeactivate');
    });
  });

  navigationTest(
    test,
    siteUrl,
    'Successfully deactivated account'
  );

  casper.run(function() {
    test.done();
  });
});