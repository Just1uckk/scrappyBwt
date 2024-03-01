from scrapy.downloadermiddlewares.retry import RetryMiddleware


class BlockedRetryMiddleware(RetryMiddleware):

    def __init__(self, settings):
        super().__init__(settings)
        self.blocked_codes = ['500', '502', '503', '504', '400', '403', '404', '408']
        self.max_retry_times = 3
        self.retry_http_codes = set(int(x) for x in self.blocked_codes)
        self.retry_blocked_codes = set(int(x) for x in self.blocked_codes)

    def process_response(self, request, response, spider):
        if response.status in self.retry_blocked_codes and not getattr(spider, 'dont_retry', None):
            retryreq = self._retry(request, "Blocked request", spider)
            if retryreq is not None:
                return retryreq
        return response

    def _retry(self, request, reason, spider):
        retries = request.meta.get('retry_times', 0) + 1
        if retries < self.max_retry_times:
            spider.logger.warning(f"Retrying {request.url} (failed {retries} times): {reason}")
            retryreq = request.copy()
            retryreq.meta['retry_times'] = retries
            retryreq.dont_filter = True
            return retryreq
        else:
            spider.logger.warning(f"Gave up retrying {request.url} (failed {retries} times): {reason}")
