cd /root/DAMG7245-Assignment3
git pull origin main
git lfs fetch
git lfs checkout
cd /root/DAMG7245-Assignment3/modelasaservice
docker-compose build
docker-compose up
