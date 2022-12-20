docker run -d --name redis-stack-server -p 1234:6379 -v "$(pwd)/redis_data:/data" redis/redis-stack-server:latest && echo "Redis started on port 1234" && exit 0
echo "Failed to start Redis" && exit 1
