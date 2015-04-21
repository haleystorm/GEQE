angular.module('NodeWebBase')
    .controller('detailsController', ['$scope','$rootScope', function ($scope, $rootScope) {
        $scope.data = null;
        $scope.currentItemIndex = null;
        $scope.displayIndex = null;
        $scope.displayCaptionHtml = "None";
        $scope.termArray = [];
        $scope.currentItem = {"usr":"unknown",
                                "cap":"none",
                                "sco":"0"};

        $rootScope.$on('loadItemData', function (event, data) {
            $scope.$apply(function () {
                $scope.data = data;
                $scope.currentItemIndex = 0;
                $scope.displayIndex = 1;
                $scope.currentItem = $scope.data.posts[0];
                $scope.displayCaptionHtml = $scope.highlightText($scope.currentItem.cap);
                $("#caption").html($scope.displayCaptionHtml);
            });
        });

        $rootScope.$on("setTermDictionary", function(event,data){
            $scope.$apply(function () {
                    angular.forEach(data,function(entry,idx){
                        $scope.termArray.push(entry[0]);
                    })
                });
        });

        $scope.highlightText = function(text){
            var words = text.split(' ');
            angular.forEach($scope.termArray,function(term,idx){
                angular.forEach(words,function(word,idx){
                    if(word.toLowerCase() == term.toLowerCase()){
                        words[idx] = '<span class="highlight">' + word + "</span>";
                    }
                    else{
                    }
                });
            });
            return words.join(' ');
        };

        $scope.next = function(){
            $scope.currentItemIndex++;

            if($scope.currentItemIndex >= $scope.data.posts.length)
                $scope.currentItemIndex = 0;

            $scope.displayIndex = $scope.currentItemIndex+1;
            $scope.currentItem = $scope.data.posts[$scope.currentItemIndex];
            $scope.displayCaptionHtml = $scope.highlightText($scope.currentItem.cap);
            $("#caption").html($scope.displayCaptionHtml);
        };

        $scope.previous = function(){
            $scope.currentItemIndex--;

            if($scope.currentItemIndex < 0)
                $scope.currentItemIndex = $scope.data.posts.length-1;

            $scope.displayIndex = $scope.currentItemIndex+1;
            $scope.currentItem = $scope.data.posts[$scope.currentItemIndex];
            $scope.displayCaptionHtml = $scope.highlightText($scope.currentItem.cap);
            $("#caption").html($scope.displayCaptionHtml);
        };

        $scope.getUser = function(){
            $.ajax({
                url:  $rootScope.baseUrl + "app/twitter/user",
                data : {
                    "screen_name":"twitterapi"
                },
                dataType: "json",
                success: function (response) {
                    $scope.user = response;
                },
                error: $rootScope.showError
            });
        };
    }]);