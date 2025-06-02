```
About
FLUX.1 Kontext [Max] -- Frontier image generation model.

1. Calling the API
#
Install the client
#
The client provides a convenient way to interact with the model API.

npmyarnpnpmbun

npm install --save @fal-ai/client
Migrate to @fal-ai/client
The @fal-ai/serverless-client package has been deprecated in favor of @fal-ai/client. Please check the migration guide for more information.

Setup your API Key
#
Set FAL_KEY as an environment variable in your runtime.


export FAL_KEY="YOUR_API_KEY"
Submit a request
#
The client API handles the API submit protocol. It will handle the request status updates and return the result when the request is completed.


import { fal } from "@fal-ai/client";

const result = await fal.subscribe("fal-ai/flux-pro/kontext/max/text-to-image", {
  input: {
    prompt: "Extreme close-up of a single tiger eye, direct frontal view. Detailed iris and pupil. Sharp focus on eye texture and color. Natural lighting to capture authentic eye shine and depth. The word \"FLUX\" is painted over it in big, white brush strokes with visible texture."
  },
  logs: true,
  onQueueUpdate: (update) => {
    if (update.status === "IN_PROGRESS") {
      update.logs.map((log) => log.message).forEach(console.log);
    }
  },
});
console.log(result.data);
console.log(result.requestId);
2. Authentication
#
The API uses an API Key for authentication. It is recommended you set the FAL_KEY environment variable in your runtime when possible.

API Key
#
In case your app is running in an environment where you cannot set environment variables, you can set the API Key manually as a client configuration.

import { fal } from "@fal-ai/client";

fal.config({
  credentials: "YOUR_FAL_KEY"
});
Protect your API Key
When running code on the client-side (e.g. in a browser, mobile app or GUI applications), make sure to not expose your FAL_KEY. Instead, use a server-side proxy to make requests to the API. For more information, check out our server-side integration guide.

3. Queue
#
Long-running requests
For long-running requests, such as training jobs or models with slower inference times, it is recommended to check the Queue status and rely on Webhooks instead of blocking while waiting for the result.

Submit a request
#
The client API provides a convenient way to submit requests to the model.


import { fal } from "@fal-ai/client";

const { request_id } = await fal.queue.submit("fal-ai/flux-pro/kontext/max/text-to-image", {
  input: {
    prompt: "Extreme close-up of a single tiger eye, direct frontal view. Detailed iris and pupil. Sharp focus on eye texture and color. Natural lighting to capture authentic eye shine and depth. The word \"FLUX\" is painted over it in big, white brush strokes with visible texture."
  },
  webhookUrl: "https://optional.webhook.url/for/results",
});
Fetch request status
#
You can fetch the status of a request to check if it is completed or still in progress.


import { fal } from "@fal-ai/client";

const status = await fal.queue.status("fal-ai/flux-pro/kontext/max/text-to-image", {
  requestId: "764cabcf-b745-4b3e-ae38-1200304cf45b",
  logs: true,
});
Get the result
#
Once the request is completed, you can fetch the result. See the Output Schema for the expected result format.


import { fal } from "@fal-ai/client";

const result = await fal.queue.result("fal-ai/flux-pro/kontext/max/text-to-image", {
  requestId: "764cabcf-b745-4b3e-ae38-1200304cf45b"
});
console.log(result.data);
console.log(result.requestId);
4. Files
#
Some attributes in the API accept file URLs as input. Whenever that's the case you can pass your own URL or a Base64 data URI.

Data URI (base64)
#
You can pass a Base64 data URI as a file input. The API will handle the file decoding for you. Keep in mind that for large files, this alternative although convenient can impact the request performance.

Hosted files (URL)
#
You can also pass your own URLs as long as they are publicly accessible. Be aware that some hosts might block cross-site requests, rate-limit, or consider the request as a bot.

Uploading files
#
We provide a convenient file storage that allows you to upload files and use them in your requests. You can upload files using the client API and use the returned URL in your requests.


import { fal } from "@fal-ai/client";

const file = new File(["Hello, World!"], "hello.txt", { type: "text/plain" });
const url = await fal.storage.upload(file);
Auto uploads
The client will auto-upload the file for you if you pass a binary object (e.g. File, Data).

Read more about file handling in our file upload guide.

5. Schema
#
Input
#
prompt string
The prompt to generate an image from.

seed integer
The same seed and the same prompt given to the same version of the model will output the same image every time.

guidance_scale float
The CFG (Classifier Free Guidance) scale is a measure of how close you want the model to stick to your prompt when looking for a related image to show you. Default value: 3.5

sync_mode boolean
If set to true, the function will wait for the image to be generated and uploaded before returning the response. This will increase the latency of the function but it allows you to get the image directly in the response without going through the CDN.

num_images integer
The number of images to generate. Default value: 1

safety_tolerance SafetyToleranceEnum
The safety tolerance level for the generated image. 1 being the most strict and 5 being the most permissive. Default value: "2"

Possible enum values: 1, 2, 3, 4, 5, 6

Note: This property is only available through API calls.

output_format OutputFormatEnum
The format of the generated image. Default value: "jpeg"

Possible enum values: jpeg, png

aspect_ratio AspectRatioEnum
The aspect ratio of the generated image. Default value: "1:1"

Possible enum values: 21:9, 16:9, 4:3, 3:2, 1:1, 2:3, 3:4, 9:16, 9:21


{
  "prompt": "Extreme close-up of a single tiger eye, direct frontal view. Detailed iris and pupil. Sharp focus on eye texture and color. Natural lighting to capture authentic eye shine and depth. The word \"FLUX\" is painted over it in big, white brush strokes with visible texture.",
  "guidance_scale": 3.5,
  "num_images": 1,
  "safety_tolerance": "2",
  "output_format": "jpeg",
  "aspect_ratio": "1:1"
}
Output
#
images list<registry__image__fast_sdxl__models__Image>
The generated image files info.

timings Timings
seed integer
Seed of the generated Image. It will be the same value of the one passed in the input or the randomly generated that was used in case none was passed.

has_nsfw_concepts list<boolean>
Whether the generated images contain NSFW concepts.

prompt string
The prompt used for generating the image.


{
  "images": [
    {
      "url": "",
      "content_type": "image/jpeg"
    }
  ],
  "prompt": ""
}
Other types
#
registry__image__fast_sdxl__models__Image
#
url string
width integer
height integer
content_type string
Default value: "image/jpeg"

FluxProRedux
#
prompt string
The prompt to generate an image from. Default value: ""

image_size ImageSize | Enum
The size of the generated image. Default value: landscape_4_3

Possible enum values: square_hd, square, portrait_4_3, portrait_16_9, landscape_4_3, landscape_16_9

Note: For custom image sizes, you can pass the width and height as an object:


"image_size": {
  "width": 1280,
  "height": 720
}
num_inference_steps integer
The number of inference steps to perform. Default value: 28

seed integer
The same seed and the same prompt given to the same version of the model will output the same image every time.

guidance_scale float
The CFG (Classifier Free Guidance) scale is a measure of how close you want the model to stick to your prompt when looking for a related image to show you. Default value: 3.5

sync_mode boolean
If set to true, the function will wait for the image to be generated and uploaded before returning the response. This will increase the latency of the function but it allows you to get the image directly in the response without going through the CDN.

num_images integer
The number of images to generate. Default value: 1

safety_tolerance SafetyToleranceEnum
The safety tolerance level for the generated image. 1 being the most strict and 5 being the most permissive. Default value: "2"

Possible enum values: 1, 2, 3, 4, 5, 6

Note: This property is only available through API calls.

output_format OutputFormatEnum
The format of the generated image. Default value: "jpeg"

Possible enum values: jpeg, png

image_url string
The image URL to generate an image from. Needs to match the dimensions of the mask.

fal__toolkit__image__image__Image
#
url string
The URL where the file can be downloaded from.

content_type string
The mime type of the file.

file_name string
The name of the file. It will be auto-generated if not provided.

file_size integer
The size of the file in bytes.

file_data string
File data

width integer
The width of the image in pixels.

height integer
The height of the image in pixels.

FluxProUltraTextToImageInputRedux
#
prompt string
The prompt to generate an image from. Default value: ""

seed integer
The same seed and the same prompt given to the same version of the model will output the same image every time.

sync_mode boolean
If set to true, the function will wait for the image to be generated and uploaded before returning the response. This will increase the latency of the function but it allows you to get the image directly in the response without going through the CDN.

num_images integer
The number of images to generate. Default value: 1

enable_safety_checker boolean
If set to true, the safety checker will be enabled. Default value: true

safety_tolerance SafetyToleranceEnum
The safety tolerance level for the generated image. 1 being the most strict and 5 being the most permissive. Default value: "2"

Possible enum values: 1, 2, 3, 4, 5, 6

Note: This property is only available through API calls.

output_format OutputFormatEnum
The format of the generated image. Default value: "jpeg"

Possible enum values: jpeg, png

aspect_ratio Enum | string
The aspect ratio of the generated image. Default value: 16:9

Possible enum values: 21:9, 16:9, 4:3, 3:2, 1:1, 2:3, 3:4, 9:16, 9:21

raw boolean
Generate less processed, more natural-looking images.

image_url string
The image URL to generate an image from. Needs to match the dimensions of the mask.

image_prompt_strength float
The strength of the image prompt, between 0 and 1. Default value: 0.1

ImageSize
#
width integer
The width of the generated image. Default value: 512

height integer
The height of the generated image. Default value: 512

Related Models
```


```
About
Experimental version of FLUX.1 Kontext [Max] with multiple images.

1. Calling the API
#
Install the client
#
The client provides a convenient way to interact with the model API.

npmyarnpnpmbun

npm install --save @fal-ai/client
Migrate to @fal-ai/client
The @fal-ai/serverless-client package has been deprecated in favor of @fal-ai/client. Please check the migration guide for more information.

Setup your API Key
#
Set FAL_KEY as an environment variable in your runtime.


export FAL_KEY="YOUR_API_KEY"
Submit a request
#
The client API handles the API submit protocol. It will handle the request status updates and return the result when the request is completed.


import { fal } from "@fal-ai/client";

const result = await fal.subscribe("fal-ai/flux-pro/kontext/max/multi", {
  input: {
    prompt: "Put the little duckling on top of the woman's t-shirt.",
    image_urls: ["https://v3.fal.media/files/penguin/XoW0qavfF-ahg-jX4BMyL_image.webp", "https://v3.fal.media/files/tiger/bml6YA7DWJXOigadvxk75_image.webp"]
  },
  logs: true,
  onQueueUpdate: (update) => {
    if (update.status === "IN_PROGRESS") {
      update.logs.map((log) => log.message).forEach(console.log);
    }
  },
});
console.log(result.data);
console.log(result.requestId);
2. Authentication
#
The API uses an API Key for authentication. It is recommended you set the FAL_KEY environment variable in your runtime when possible.

API Key
#
In case your app is running in an environment where you cannot set environment variables, you can set the API Key manually as a client configuration.

import { fal } from "@fal-ai/client";

fal.config({
  credentials: "YOUR_FAL_KEY"
});
Protect your API Key
When running code on the client-side (e.g. in a browser, mobile app or GUI applications), make sure to not expose your FAL_KEY. Instead, use a server-side proxy to make requests to the API. For more information, check out our server-side integration guide.

3. Queue
#
Long-running requests
For long-running requests, such as training jobs or models with slower inference times, it is recommended to check the Queue status and rely on Webhooks instead of blocking while waiting for the result.

Submit a request
#
The client API provides a convenient way to submit requests to the model.


import { fal } from "@fal-ai/client";

const { request_id } = await fal.queue.submit("fal-ai/flux-pro/kontext/max/multi", {
  input: {
    prompt: "Put the little duckling on top of the woman's t-shirt.",
    image_urls: ["https://v3.fal.media/files/penguin/XoW0qavfF-ahg-jX4BMyL_image.webp", "https://v3.fal.media/files/tiger/bml6YA7DWJXOigadvxk75_image.webp"]
  },
  webhookUrl: "https://optional.webhook.url/for/results",
});
Fetch request status
#
You can fetch the status of a request to check if it is completed or still in progress.


import { fal } from "@fal-ai/client";

const status = await fal.queue.status("fal-ai/flux-pro/kontext/max/multi", {
  requestId: "764cabcf-b745-4b3e-ae38-1200304cf45b",
  logs: true,
});
Get the result
#
Once the request is completed, you can fetch the result. See the Output Schema for the expected result format.


import { fal } from "@fal-ai/client";

const result = await fal.queue.result("fal-ai/flux-pro/kontext/max/multi", {
  requestId: "764cabcf-b745-4b3e-ae38-1200304cf45b"
});
console.log(result.data);
console.log(result.requestId);
4. Files
#
Some attributes in the API accept file URLs as input. Whenever that's the case you can pass your own URL or a Base64 data URI.

Data URI (base64)
#
You can pass a Base64 data URI as a file input. The API will handle the file decoding for you. Keep in mind that for large files, this alternative although convenient can impact the request performance.

Hosted files (URL)
#
You can also pass your own URLs as long as they are publicly accessible. Be aware that some hosts might block cross-site requests, rate-limit, or consider the request as a bot.

Uploading files
#
We provide a convenient file storage that allows you to upload files and use them in your requests. You can upload files using the client API and use the returned URL in your requests.


import { fal } from "@fal-ai/client";

const file = new File(["Hello, World!"], "hello.txt", { type: "text/plain" });
const url = await fal.storage.upload(file);
Auto uploads
The client will auto-upload the file for you if you pass a binary object (e.g. File, Data).

Read more about file handling in our file upload guide.

5. Schema
#
Input
#
prompt string
The prompt to generate an image from.

seed integer
The same seed and the same prompt given to the same version of the model will output the same image every time.

guidance_scale float
The CFG (Classifier Free Guidance) scale is a measure of how close you want the model to stick to your prompt when looking for a related image to show you. Default value: 3.5

sync_mode boolean
If set to true, the function will wait for the image to be generated and uploaded before returning the response. This will increase the latency of the function but it allows you to get the image directly in the response without going through the CDN.

num_images integer
The number of images to generate. Default value: 1

safety_tolerance SafetyToleranceEnum
The safety tolerance level for the generated image. 1 being the most strict and 5 being the most permissive. Default value: "2"

Possible enum values: 1, 2, 3, 4, 5, 6

Note: This property is only available through API calls.

output_format OutputFormatEnum
The format of the generated image. Default value: "jpeg"

Possible enum values: jpeg, png

aspect_ratio AspectRatioEnum
The aspect ratio of the generated image.

Possible enum values: 21:9, 16:9, 4:3, 3:2, 1:1, 2:3, 3:4, 9:16, 9:21

image_urls list<string>
Image prompt for the omni model.


{
  "prompt": "Put the little duckling on top of the woman's t-shirt.",
  "guidance_scale": 3.5,
  "num_images": 1,
  "safety_tolerance": "2",
  "output_format": "jpeg",
  "image_urls": [
    "https://v3.fal.media/files/penguin/XoW0qavfF-ahg-jX4BMyL_image.webp",
    "https://v3.fal.media/files/tiger/bml6YA7DWJXOigadvxk75_image.webp"
  ]
}
Output
#
images list<registry__image__fast_sdxl__models__Image>
The generated image files info.

timings Timings
seed integer
Seed of the generated Image. It will be the same value of the one passed in the input or the randomly generated that was used in case none was passed.

has_nsfw_concepts list<boolean>
Whether the generated images contain NSFW concepts.

prompt string
The prompt used for generating the image.


{
  "images": [
    {
      "url": "",
      "content_type": "image/jpeg"
    }
  ],
  "prompt": ""
}
Other types
#
registry__image__fast_sdxl__models__Image
#
url string
width integer
height integer
content_type string
Default value: "image/jpeg"

FluxProRedux
#
prompt string
The prompt to generate an image from. Default value: ""

image_size ImageSize | Enum
The size of the generated image. Default value: landscape_4_3

Possible enum values: square_hd, square, portrait_4_3, portrait_16_9, landscape_4_3, landscape_16_9

Note: For custom image sizes, you can pass the width and height as an object:


"image_size": {
  "width": 1280,
  "height": 720
}
num_inference_steps integer
The number of inference steps to perform. Default value: 28

seed integer
The same seed and the same prompt given to the same version of the model will output the same image every time.

guidance_scale float
The CFG (Classifier Free Guidance) scale is a measure of how close you want the model to stick to your prompt when looking for a related image to show you. Default value: 3.5

sync_mode boolean
If set to true, the function will wait for the image to be generated and uploaded before returning the response. This will increase the latency of the function but it allows you to get the image directly in the response without going through the CDN.

num_images integer
The number of images to generate. Default value: 1

safety_tolerance SafetyToleranceEnum
The safety tolerance level for the generated image. 1 being the most strict and 5 being the most permissive. Default value: "2"

Possible enum values: 1, 2, 3, 4, 5, 6

Note: This property is only available through API calls.

output_format OutputFormatEnum
The format of the generated image. Default value: "jpeg"

Possible enum values: jpeg, png

image_url string
The image URL to generate an image from. Needs to match the dimensions of the mask.

fal__toolkit__image__image__Image
#
url string
The URL where the file can be downloaded from.

content_type string
The mime type of the file.

file_name string
The name of the file. It will be auto-generated if not provided.

file_size integer
The size of the file in bytes.

file_data string
File data

width integer
The width of the image in pixels.

height integer
The height of the image in pixels.

FluxProUltraTextToImageInputRedux
#
prompt string
The prompt to generate an image from. Default value: ""

seed integer
The same seed and the same prompt given to the same version of the model will output the same image every time.

sync_mode boolean
If set to true, the function will wait for the image to be generated and uploaded before returning the response. This will increase the latency of the function but it allows you to get the image directly in the response without going through the CDN.

num_images integer
The number of images to generate. Default value: 1

enable_safety_checker boolean
If set to true, the safety checker will be enabled. Default value: true

safety_tolerance SafetyToleranceEnum
The safety tolerance level for the generated image. 1 being the most strict and 5 being the most permissive. Default value: "2"

Possible enum values: 1, 2, 3, 4, 5, 6

Note: This property is only available through API calls.

output_format OutputFormatEnum
The format of the generated image. Default value: "jpeg"

Possible enum values: jpeg, png

aspect_ratio Enum | string
The aspect ratio of the generated image. Default value: 16:9

Possible enum values: 21:9, 16:9, 4:3, 3:2, 1:1, 2:3, 3:4, 9:16, 9:21

raw boolean
Generate less processed, more natural-looking images.

image_url string
The image URL to generate an image from. Needs to match the dimensions of the mask.

image_prompt_strength float
The strength of the image prompt, between 0 and 1. Default value: 0.1

ImageSize
#
width integer
The width of the generated image. Default value: 512

height integer
The height of the generated image. Default value: 512

FluxProTextToImageInputWithAR
#
prompt string
The prompt to generate an image from.

seed integer
The same seed and the same prompt given to the same version of the model will output the same image every time.

guidance_scale float
The CFG (Classifier Free Guidance) scale is a measure of how close you want the model to stick to your prompt when looking for a related image to show you. Default value: 3.5

sync_mode boolean
If set to true, the function will wait for the image to be generated and uploaded before returning the response. This will increase the latency of the function but it allows you to get the image directly in the response without going through the CDN.

num_images integer
The number of images to generate. Default value: 1

safety_tolerance SafetyToleranceEnum
The safety tolerance level for the generated image. 1 being the most strict and 5 being the most permissive. Default value: "2"

Possible enum values: 1, 2, 3, 4, 5, 6

Note: This property is only available through API calls.

output_format OutputFormatEnum
The format of the generated image. Default value: "jpeg"

Possible enum values: jpeg, png

aspect_ratio AspectRatioEnum
The aspect ratio of the generated image. Default value: "1:1"

Possible enum values: 21:9, 16:9, 4:3, 3:2, 1:1, 2:3, 3:4, 9:16, 9:21

Related Models
```

```
About
FLUX.1 Kontext [pro] -- Frontier image editing model.

Kontext makes editing images easy! Specify what you want to change and Kontext will follow. It is capable of understanding the context of the image, making it easier to edit them without having to describe in details what you want to do.

1. Calling the API
#
Install the client
#
The client provides a convenient way to interact with the model API.

npmyarnpnpmbun

npm install --save @fal-ai/client
Migrate to @fal-ai/client
The @fal-ai/serverless-client package has been deprecated in favor of @fal-ai/client. Please check the migration guide for more information.

Setup your API Key
#
Set FAL_KEY as an environment variable in your runtime.


export FAL_KEY="YOUR_API_KEY"
Submit a request
#
The client API handles the API submit protocol. It will handle the request status updates and return the result when the request is completed.


import { fal } from "@fal-ai/client";

const result = await fal.subscribe("fal-ai/flux-pro/kontext", {
  input: {
    prompt: "Put a donut next to the flour.",
    image_url: "https://v3.fal.media/files/rabbit/rmgBxhwGYb2d3pl3x9sKf_output.png"
  },
  logs: true,
  onQueueUpdate: (update) => {
    if (update.status === "IN_PROGRESS") {
      update.logs.map((log) => log.message).forEach(console.log);
    }
  },
});
console.log(result.data);
console.log(result.requestId);
2. Authentication
#
The API uses an API Key for authentication. It is recommended you set the FAL_KEY environment variable in your runtime when possible.

API Key
#
In case your app is running in an environment where you cannot set environment variables, you can set the API Key manually as a client configuration.

import { fal } from "@fal-ai/client";

fal.config({
  credentials: "YOUR_FAL_KEY"
});
Protect your API Key
When running code on the client-side (e.g. in a browser, mobile app or GUI applications), make sure to not expose your FAL_KEY. Instead, use a server-side proxy to make requests to the API. For more information, check out our server-side integration guide.

3. Queue
#
Long-running requests
For long-running requests, such as training jobs or models with slower inference times, it is recommended to check the Queue status and rely on Webhooks instead of blocking while waiting for the result.

Submit a request
#
The client API provides a convenient way to submit requests to the model.


import { fal } from "@fal-ai/client";

const { request_id } = await fal.queue.submit("fal-ai/flux-pro/kontext", {
  input: {
    prompt: "Put a donut next to the flour.",
    image_url: "https://v3.fal.media/files/rabbit/rmgBxhwGYb2d3pl3x9sKf_output.png"
  },
  webhookUrl: "https://optional.webhook.url/for/results",
});
Fetch request status
#
You can fetch the status of a request to check if it is completed or still in progress.


import { fal } from "@fal-ai/client";

const status = await fal.queue.status("fal-ai/flux-pro/kontext", {
  requestId: "764cabcf-b745-4b3e-ae38-1200304cf45b",
  logs: true,
});
Get the result
#
Once the request is completed, you can fetch the result. See the Output Schema for the expected result format.


import { fal } from "@fal-ai/client";

const result = await fal.queue.result("fal-ai/flux-pro/kontext", {
  requestId: "764cabcf-b745-4b3e-ae38-1200304cf45b"
});
console.log(result.data);
console.log(result.requestId);
4. Files
#
Some attributes in the API accept file URLs as input. Whenever that's the case you can pass your own URL or a Base64 data URI.

Data URI (base64)
#
You can pass a Base64 data URI as a file input. The API will handle the file decoding for you. Keep in mind that for large files, this alternative although convenient can impact the request performance.

Hosted files (URL)
#
You can also pass your own URLs as long as they are publicly accessible. Be aware that some hosts might block cross-site requests, rate-limit, or consider the request as a bot.

Uploading files
#
We provide a convenient file storage that allows you to upload files and use them in your requests. You can upload files using the client API and use the returned URL in your requests.


import { fal } from "@fal-ai/client";

const file = new File(["Hello, World!"], "hello.txt", { type: "text/plain" });
const url = await fal.storage.upload(file);
Auto uploads
The client will auto-upload the file for you if you pass a binary object (e.g. File, Data).

Read more about file handling in our file upload guide.

5. Schema
#
Input
#
prompt string
The prompt to generate an image from.

seed integer
The same seed and the same prompt given to the same version of the model will output the same image every time.

guidance_scale float
The CFG (Classifier Free Guidance) scale is a measure of how close you want the model to stick to your prompt when looking for a related image to show you. Default value: 3.5

sync_mode boolean
If set to true, the function will wait for the image to be generated and uploaded before returning the response. This will increase the latency of the function but it allows you to get the image directly in the response without going through the CDN.

num_images integer
The number of images to generate. Default value: 1

safety_tolerance SafetyToleranceEnum
The safety tolerance level for the generated image. 1 being the most strict and 5 being the most permissive. Default value: "2"

Possible enum values: 1, 2, 3, 4, 5, 6

Note: This property is only available through API calls.

output_format OutputFormatEnum
The format of the generated image. Default value: "jpeg"

Possible enum values: jpeg, png

aspect_ratio AspectRatioEnum
The aspect ratio of the generated image.

Possible enum values: 21:9, 16:9, 4:3, 3:2, 1:1, 2:3, 3:4, 9:16, 9:21

image_url string
Image prompt for the omni model.


{
  "prompt": "Put a donut next to the flour.",
  "guidance_scale": 3.5,
  "num_images": 1,
  "safety_tolerance": "2",
  "output_format": "jpeg",
  "image_url": "https://v3.fal.media/files/rabbit/rmgBxhwGYb2d3pl3x9sKf_output.png"
}
Output
#
images list<fal__toolkit__image__image__Image>
The generated image files info.

timings Timings
seed integer
Seed of the generated Image. It will be the same value of the one passed in the input or the randomly generated that was used in case none was passed.

has_nsfw_concepts list<boolean>
Whether the generated images contain NSFW concepts.

prompt string
The prompt used for generating the image.


{
  "images": [
    {
      "height": 1024,
      "url": "https://fal.media/files/tiger/7dSJbIU_Ni-0Zp9eaLsvR_fe56916811d84ac69c6ffc0d32dca151.jpg",
      "width": 1024
    }
  ],
  "prompt": ""
}
Other types
#
registry__image__fast_sdxl__models__Image
#
url string
width integer
height integer
content_type string
Default value: "image/jpeg"

FluxProRedux
#
prompt string
The prompt to generate an image from. Default value: ""

image_size ImageSize | Enum
The size of the generated image. Default value: landscape_4_3

Possible enum values: square_hd, square, portrait_4_3, portrait_16_9, landscape_4_3, landscape_16_9

Note: For custom image sizes, you can pass the width and height as an object:


"image_size": {
  "width": 1280,
  "height": 720
}
num_inference_steps integer
The number of inference steps to perform. Default value: 28

seed integer
The same seed and the same prompt given to the same version of the model will output the same image every time.

guidance_scale float
The CFG (Classifier Free Guidance) scale is a measure of how close you want the model to stick to your prompt when looking for a related image to show you. Default value: 3.5

sync_mode boolean
If set to true, the function will wait for the image to be generated and uploaded before returning the response. This will increase the latency of the function but it allows you to get the image directly in the response without going through the CDN.

num_images integer
The number of images to generate. Default value: 1

safety_tolerance SafetyToleranceEnum
The safety tolerance level for the generated image. 1 being the most strict and 5 being the most permissive. Default value: "2"

Possible enum values: 1, 2, 3, 4, 5, 6

Note: This property is only available through API calls.

output_format OutputFormatEnum
The format of the generated image. Default value: "jpeg"

Possible enum values: jpeg, png

image_url string
The image URL to generate an image from. Needs to match the dimensions of the mask.

fal__toolkit__image__image__Image
#
url string
The URL where the file can be downloaded from.

content_type string
The mime type of the file.

file_name string
The name of the file. It will be auto-generated if not provided.

file_size integer
The size of the file in bytes.

file_data string
File data

width integer
The width of the image in pixels.

height integer
The height of the image in pixels.

FluxProUltraTextToImageInputRedux
#
prompt string
The prompt to generate an image from. Default value: ""

seed integer
The same seed and the same prompt given to the same version of the model will output the same image every time.

sync_mode boolean
If set to true, the function will wait for the image to be generated and uploaded before returning the response. This will increase the latency of the function but it allows you to get the image directly in the response without going through the CDN.

num_images integer
The number of images to generate. Default value: 1

enable_safety_checker boolean
If set to true, the safety checker will be enabled. Default value: true

safety_tolerance SafetyToleranceEnum
The safety tolerance level for the generated image. 1 being the most strict and 5 being the most permissive. Default value: "2"

Possible enum values: 1, 2, 3, 4, 5, 6

Note: This property is only available through API calls.

output_format OutputFormatEnum
The format of the generated image. Default value: "jpeg"

Possible enum values: jpeg, png

aspect_ratio Enum | string
The aspect ratio of the generated image. Default value: 16:9

Possible enum values: 21:9, 16:9, 4:3, 3:2, 1:1, 2:3, 3:4, 9:16, 9:21

raw boolean
Generate less processed, more natural-looking images.

image_url string
The image URL to generate an image from. Needs to match the dimensions of the mask.

image_prompt_strength float
The strength of the image prompt, between 0 and 1. Default value: 0.1

ImageSize
#
width integer
The width of the generated image. Default value: 512

height integer
The height of the generated image. Default value: 512

FluxProTextToImageInputWithAR
#
prompt string
The prompt to generate an image from.

seed integer
The same seed and the same prompt given to the same version of the model will output the same image every time.

guidance_scale float
The CFG (Classifier Free Guidance) scale is a measure of how close you want the model to stick to your prompt when looking for a related image to show you. Default value: 3.5

sync_mode boolean
If set to true, the function will wait for the image to be generated and uploaded before returning the response. This will increase the latency of the function but it allows you to get the image directly in the response without going through the CDN.

num_images integer
The number of images to generate. Default value: 1

safety_tolerance SafetyToleranceEnum
The safety tolerance level for the generated image. 1 being the most strict and 5 being the most permissive. Default value: "2"

Possible enum values: 1, 2, 3, 4, 5, 6

Note: This property is only available through API calls.

output_format OutputFormatEnum
The format of the generated image. Default value: "jpeg"

Possible enum values: jpeg, png

aspect_ratio AspectRatioEnum
The aspect ratio of the generated image. Default value: "1:1"

Possible enum values: 21:9, 16:9, 4:3, 3:2, 1:1, 2:3, 3:4, 9:16, 9:21

Related Models
```
