#!/bin/sh

echo "🎚️ Setting up audio mixer..."

# Enable DAC to headphone output
amixer sset 'Left Headphone Mixer Left DAC' on
amixer sset 'Right Headphone Mixer Right DAC' on
amixer sset 'Headphone' unmute
amixer sset 'Headphone' 100%



echo "🔄 Waiting for hassio_audio container to start..."

# Loop until the hassio_audio container is found
while [ -z "$CONTAINER_ID" ]; do
  CONTAINER_ID=$(docker ps --filter "name=hassio_audio" --format "{{.ID}}")
  if [ -z "$CONTAINER_ID" ]; then
    echo "⏳ hassio_audio not found, retrying in 5 seconds..."
    sleep 5
  fi
done

log "✅ Found hassio_audio container: $CONTAINER_ID"
sleep 5

# Rename pulseaudio binary inside the container
docker exec -i "$CONTAINER_ID" mv /usr/bin/pulseaudio /usr/bin/pulseaudio.disabled

# Kill any running pulseaudio process
docker exec -i "$CONTAINER_ID" killall -9 pulseaudio

echo "✅ Mixer configured, starting TTS listener..."

# Run the Python TTS listener
exec python3 /tts-mqtt.py
