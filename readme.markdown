# arby

Hypermedia directives for bitcoin arbitrage

##MVP

1. Intra- and Inter-exchange arbitrage

##Front end ideas

    URL: ./charge/
    METHOD: post

    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <title></title>
      <script>
        controller('paymentSection', [
          '$scope',
          '$q'
          ($scope, $q, $http) ->
            console.log $scope
            $scope.goToGoogle = () ->
              count = 0
              arrOfVoters = [
                () ->
                  return $http.get('http://endpointProfile1')
                () ->
                  return $http.get('http://endpointProfile2')
                () ->
                  return $http.get('http://endpointProfile3')
                () ->
                  return $http.get('http://endpointProfile4')
              ]
              d = $q.all arrOfVoters

              d.then (data) ->
                if data.count > .65
                  window.location.href = $scope.purchase.nextPage
        ])
      </script>
    </head>
    <body>
      <div ctrl="">
      <button
        data-purchase="{
          nextPage: 'http://google.com'
        }"
        onclick="goToGoogle()"
      >
          Go to Google if voter endpoints suggest that
          should be the next site the next user sees
      </button>
    </body>
    </html>

## TODO

1. Set up angularFire and angularfire-generator through Yeoman.
   Build out Directives, etc.
2. Wrap with angularAMD and angularamd-generator.
3. pygraphviz, etc.
4. Rickshaw or D3+c3.
5. twisted to automate posts to Firebase instance.
6. BreezeJS wrappers for factories (data mode) and services layer.
