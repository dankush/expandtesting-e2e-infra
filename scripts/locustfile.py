from locust import HttpUser, task, between, events
from statistics import mean

# Performance thresholds
MAX_AVG_RESPONSE_TIME = 500  # Maximum allowed average response time in ms
MIN_SUCCESS_RATE = 99.0  # Minimum acceptable success rate in percentage
MIN_RPS = 4.0  # Minimum required Requests Per Second (RPS)

class HealthCheckTest(HttpUser):
    host = "https://practice.expandtesting.com/notes/api"
    wait_time = between(1, 3)  # Simulates real user wait times

    response_times = []

    @task
    def health_check(self):
        """Task: Check API health and record response times."""
        response = self.client.get("/health-check")

        # Store response time in milliseconds
        self.response_times.append(response.elapsed.total_seconds() * 1000)  # Convert to ms

    @events.quitting.add_listener
    def validate_results(environment, **kwargs):
        """Perform assertions when Locust finishes running."""
        total_requests = environment.stats.total.num_requests
        total_failures = environment.stats.total.num_failures

        if total_requests == 0:
            print("\nNo requests were made! Test failed.")
            environment.process_exit_code = 1
            return

        avg_response_time = mean(HealthCheckTest.response_times) if HealthCheckTest.response_times else 0
        success_rate = (1 - (total_failures / total_requests)) * 100 if total_requests > 0 else 0
        rps = environment.runner.stats.total.current_rps if environment.runner else 0

        print("\nPerformance Test Summary")
        print(f"Total Requests: {total_requests}")
        print(f"Success Rate: {success_rate:.2f}% (Failures: {total_failures})")
        print(f"Average Response Time: {avg_response_time:.2f} ms")
        print(f"Requests per Second (RPS): {rps:.2f}")

        # Assertions
        failed = False

        if avg_response_time > MAX_AVG_RESPONSE_TIME:
            print(f"FAIL: Average response time {avg_response_time:.2f} ms exceeds {MAX_AVG_RESPONSE_TIME} ms")
            failed = True

        if success_rate < MIN_SUCCESS_RATE:
            print(f"FAIL: Success rate {success_rate:.2f}% is below {MIN_SUCCESS_RATE}%")
            failed = True

        if rps < MIN_RPS:
            print(f"FAIL: RPS {rps:.2f} is below {MIN_RPS}")
            failed = True

        if failed:
            environment.process_exit_code = 1
        else:
            print("PASS: All performance criteria met!")
            environment.process_exit_code = 0