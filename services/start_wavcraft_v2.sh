export AUDIOSEP_SERVICE_PORT=$((${SERVICE_PORT}+2))

conda activate AudioSep
nohup python3 services/audiosep_service_v2.py > services_logs/audiosep_v2.out 2>&1 &
echo "AudioSep is loaded sucessfully."