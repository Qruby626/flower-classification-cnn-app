import numpy as np
import keras
import cv2
import os
import tensorflow as tf

# Cache for grad_model to improve performance
_grad_model_cache = {}

def get_gradcam_heatmap(model, img_array, last_conv_layer_name, pred_index=None):
    """
    Generates a Grad-CAM heatmap for a given image and layer using Keras 3 and TensorFlow.
    """
    global _grad_model_cache
    
    # Simple cache key
    cache_key = (id(model), last_conv_layer_name)
    
    if cache_key in _grad_model_cache:
        grad_model = _grad_model_cache[cache_key]
    else:
        try:
            # Create a model that maps the input image to the activations
            # of the last conv layer as well as the output predictions
            grad_model = keras.models.Model(
                inputs=[model.inputs],
                outputs=[model.get_layer(last_conv_layer_name).output, model.output]
            )
        except Exception:
            # Fallback: manually find the last conv layer
            last_conv_layer = None
            for layer in reversed(model.layers):
                if isinstance(layer, keras.Model):
                    # Dig into nested base model (like MobileNetV2)
                    for l in reversed(layer.layers):
                        if 'conv' in l.name.lower() or l.name.lower() == last_conv_layer_name:
                            last_conv_layer = l
                            break
                if last_conv_layer: break
                if 'conv' in layer.name.lower() or layer.name.lower() == last_conv_layer_name:
                    last_conv_layer = layer
                    break
            
            if last_conv_layer is None:
                return None
                
            grad_model = keras.models.Model(
                inputs=[model.inputs],
                outputs=[last_conv_layer.output, model.output]
            )
        
        # Save to cache
        _grad_model_cache[cache_key] = grad_model

    # We use tf.GradientTape for the gradient calculation
    with tf.GradientTape() as tape:
        last_conv_layer_output, preds = grad_model(img_array)
        
        # Keras 3 might return list/tuple for multiple outputs
        if isinstance(preds, (list, tuple)):
            preds = preds[0]
        if isinstance(last_conv_layer_output, (list, tuple)):
            last_conv_layer_output = last_conv_layer_output[0]

        if pred_index is None:
            pred_index = keras.ops.argmax(preds[0])
        
        # Use keras.ops for robust indexing
        class_channel = preds[:, pred_index]

    # This is the gradient of the output neuron with regard to the output feature map
    grads = tape.gradient(class_channel, last_conv_layer_output)

    # Mean intensity of the gradient over a specific feature map channel
    # Keras 3 ops.mean is backend agnostic
    pooled_grads = keras.ops.mean(grads, axis=(0, 1, 2))

    # Multiply each channel in the feature map by "how important this channel is"
    # Ensure we are using the first sample in the batch
    if len(last_conv_layer_output.shape) == 4:
        last_conv_layer_output = last_conv_layer_output[0]
    
    # Use keras ops for matmul (using @ for ops is supported in Keras 3)
    heatmap = last_conv_layer_output @ pooled_grads[..., None]
    heatmap = keras.ops.squeeze(heatmap)

    # Normalize the heatmap between 0 & 1
    # Adding epsilon to avoid division by zero
    heatmap = keras.ops.maximum(heatmap, 0) / (keras.ops.max(heatmap) + 1e-10)
    
    # Convert to numpy array
    return keras.ops.convert_to_numpy(heatmap)

def save_and_display_gradcam(img_path, heatmap, cam_path="cam.jpg", alpha=0.4):
    # Load the original image
    img = cv2.imread(img_path)
    if img is None: return None
    
    # Rescale heatmap to a range 0-255
    heatmap = np.uint8(255 * heatmap)

    # Use jet colormap to colorize heatmap
    jet = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)

    # Resize heatmap to match original image size
    jet = cv2.resize(jet, (img.shape[1], img.shape[0]))

    # Superimpose the heatmap on original image
    superimposed_img = jet * alpha + img
    superimposed_img = np.clip(superimposed_img, 0, 255).astype(np.uint8)

    # Save the superimposed image
    cv2.imwrite(cam_path, superimposed_img)
    return cam_path
