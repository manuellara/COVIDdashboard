# Docker image name
$imageName = "covid"


# if image exists then run image, else build image then run
if ("$(docker images -q $imageName)"){
  # runs container then removes it after its complete
  docker run -d --rm --env-file .env $imageName

  Write-Host "$imageName sync container was run successfully"
}
else {
  Write-Host "$imageName does not exists. Will attempt to build Docker image"

  # builds image 
  docker build -t $imageName .

  Write-Host "Docker image $imageName build complete."

  Write-Host "Attempting to run..."

  docker run -d --rm --env-file .env $imageName
}

