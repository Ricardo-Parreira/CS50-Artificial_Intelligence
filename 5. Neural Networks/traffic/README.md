At first, I tried with a simple dense layer with 64 neurons between the input and output as it was what was documented 
in the keras documentation. This alone already showed good results. At the ebd of the 10th epoch it was already scoring an accuracy 
of 0.9961 in the small data set.
Then I tried adding a max pool before flattening it but it didn't change the accuracy much. The real change came when I added
a 2D convolution layer after the input, there the accuracy was a nice round 1.000 in the small dataset. Only needing 4 epochs to reach this perfect score.
Of course this was still not enough to score satisfactory in the large dataset.
Seeing as the Conv2D layer was so useful before I added another one before flattening the array and the change was drastic
taking the accuracy to a 0.9774. After that I tried adding more neurons to this layer but the accuracy went up only a decimal and the time doubled so I reverted to 32 neurons.
Curiously adding a new dense layer only made the accuracy decrease.
Lastly after experimenting some more, the best I could do without sacrificing a lot of time was a balance between relu and sigmoid activation on the layers and remove the dense ones.
With that i was able to reach 0.9987 accuracy on the large data-set.