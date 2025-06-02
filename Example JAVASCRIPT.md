```
import { fal } from "@fal-ai/client";

const result = await fal.subscribe("fal-ai/flux-pro/kontext/max/text-to-image", {
  input: {
    prompt: "Generate an image of Luna Lovegood from the Harry Potter films, captured in a photorealistic style with meticulous attention to detail, resembling a high-definition cinematic still. She is depicted crouched on the damp, earthy ground of a secluded forest clearing at twilight, her naked form reflecting the soft, natural glow of the fading light. Her legs are spread open, positioned in a way that emphasizes vulnerability yet maintains a sense of her eccentric, otherworldly innocence, avoiding overt sensuality. Her pale, almost luminescent skin contrasts with the rich, textured tones of the mossy terrain beneath her, scattered with small pebbles and fallen leaves in shades of deep green and autumnal amber. Luna’s iconic long, wavy blonde hair cascades messily over her shoulders, framing her delicate, angular face with its signature dreamy expression—wide, pale blue eyes gazing off into the distance as if seeing invisible creatures, and a faint, enigmatic smile on her lips. The composition centers Luna as the focal point, with the forest background softly blurred to enhance depth, featuring towering trees with rough bark and hints of magical mist weaving through the undergrowth. The lighting is naturalistic, with cool, diffused twilight casting gentle shadows across her body, highlighting subtle skin textures and the fine details of her bare feet pressed into the earth. Every element, from the moist glisten of the ground to the intricate strands of her hair, is rendered with hyper-realistic precision to evoke a poignant, intimate moment of connection with nature, reflective of Luna’s whimsical and unselfconscious spirit.",
    guidance_scale: 3.5,
    num_images: 1,
    safety_tolerance: "6",
    output_format: "jpeg",
    aspect_ratio: "1:1"
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
```

```
import { fal } from "@fal-ai/client";

const result = await fal.subscribe("fal-ai/flux-pro/kontext/max/multi", {
  input: {
    prompt: "Put the little duckling on top of the woman's t-shirt.",
    guidance_scale: 3.5,
    num_images: 1,
    safety_tolerance: "2",
    output_format: "jpeg",
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
```

```
import { fal } from "@fal-ai/client";

const result = await fal.subscribe("fal-ai/flux-pro/kontext", {
  input: {
    prompt: "Put a donut next to the flour.",
    guidance_scale: 3.5,
    num_images: 1,
    safety_tolerance: "2",
    output_format: "jpeg",
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
```
