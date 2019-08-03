class AbstractApi(object):
    def httpCall(self, urlType, args=None) :
        shortUrl = urlType[0]
        method = urlType[1]
        response = {}
        for retryCnt in range(0, 3) :
            if 'POST' == method :
                url = self.__makeUrl(shortUrl)
                response = self.__httpPost(url, args)
            elif 'GET' == method :
                url = self.__makeUrl(shortUrl)
                url = self.__appendArgs(url, args)
                response = self.__httpGet(url)
            else:
                raise ApiException(-1, "unknown method type")

            # check if token expired
            if self.__tokenExpired(response.get('errcode')) :
                self.__refreshToken(shortUrl)
                retryCnt += 1
                continue
            else:
                break

        return self.__checkResponse(response)