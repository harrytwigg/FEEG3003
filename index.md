## Adjustable Singing Synthesis Using Machine Learning

<em>Using DDSP to learn and synthesize singing with adjustable latent space parameters</em>

2 models were created one for each of the artists Coldplay and Taylor Swift.

### Unmodified Inference

A sample was re-created with no latent space parameters adjusted. This was done to gauge the performance of the model.

<audio ref='Original Frame' src="https://raw.githubusercontent.com/harrytwigg/FEEG3003/master/vendor/results/Coldplay/original_frame.wav"></audio>


### Pitch Transposition

This test involved transposing F0 across the sample by an octave amount, so that the underlying tune was transposed by an octave. Sampes were transposed by -2, -1, 0 (unmodified inference), +0.5, +1, +2 octaves.

### Constant F0

F0 was set as constant throughout the sample as, the F0 value chosen was the average of the F0 values in the sample, however any value could have been used.

### Timbral Transfer Test

The female voice model (Tylor Swift) was applied to other unseen artists to evalute the generality of the model.

### Separation of Vocals

Vocals were separated from the original track with instrrumentals

### Links

The Code:

https://github.com/harrytwigg/FEEG3003/

The Paper:

https://1drv.ms/b/s!ArIPg_vhs6CEov5SBq-GE2DUf9SjJg?e=fAapvd

Training Models and Datasets:

https://drive.google.com/drive/folders/1CWdEco9tJ5fNBZfvLGqbSrfdYQ6pLZsz?usp=sharing