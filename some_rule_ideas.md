Here you go sir dude — a **clean catalog of biologically-plausible, simulation-friendly neural mechanics**, written in your intuitive language (boredom, tiredness, spreading hairs, etc.). This is exactly the toolkit you can mix-and-match to build your “living” neural tissue.

---

# **I. Synapse-level mechanics (connection behaviors)**

## **1. Habituation (boredom)**

Repeated stimulation → synapse weakens.

* Prevents overreaction
* Detects novelty
* Great primitive learning rule

**Rule:**
`weight -= k * recent_activity`

---

## **2. Sensitization (heightened reaction)**

Opposite of habituation:
If a connection rarely fires then suddenly gets a strong input, it temporarily becomes **extra** responsive.

Useful for:

* alert responses
* threat detection
* sudden stimuli

**Rule:**
`weight += bonus if big spike arrives after quiet period`

---

## **3. Short-term plasticity (fatigue)**

Repeated rapid firing → synapse temporarily weakens **for seconds**.

Think:
“Signal line gets tired.”

Two variants:

### Facilitation

* First spike small
* Subsequent spikes bigger
* Then exhaustion

### Depression

* First spike big
* Subsequent spikes smaller

**Rule:** synapse has a “resource pool” that drains/recovers.

---

## **4. Long-term potentiation (LTP)**

If two neurons fire together often → connection permanently strengthens.

Very slow:

* minutes to hours

**Rule:**
`weight += small * correlation`

---

## **5. Long-term depression (LTD)**

Inverse: persistent anti-correlation weakens connection long-term.

**Rule:**
`weight -= small * anti_correlation`

---

## **6. Synapse drift**

All weights drift up/down slowly even without activity.

This is a stabilizer and source of randomness.

**Rule:**
`weight += noise or slow_decay`

---

## **7. Synapse pruning**

If a connection stays weak/unused for a long time → it dies.

Useful for:

* self-cleaning the network
* making structure more efficient

**Rule:**
`if weight < tiny for long enough: remove synapse`

---

## **8. Synapse growth / sprouting**

Dendrites and axons spontaneously try new tiny connections.

* Explore new structure
* Find new neighbors
* Very important for plasticity

**Rule:**
Every X ticks, give each dendrite a chance to grow a small segment.

---

# **II. Axon-level mechanics (sender behaviors)**

## **9. Axon branching**

Axons can grow new sub-branches toward active regions.

**Rule:**
When neuron fires strongly & repeatedly:

* extend a branch slightly toward recent sources of stimulation

---

## **10. Axon retraction**

If regions around the axon stay quiet, branches retract.

**Rule:**
Aging-out inactive branches.

---

## **11. Axon guidance (movement)**

Axon tips move toward:

* gradients of activity
* chemical attractors
* specific cell types

In your sim:
**axon endpoints slowly drift toward active sites.**

---

## **12. Axon “hairs” (filopodia)**

Yes — axons have little probing hairs.

These hairs:

* randomly wiggle
* search for dendrites
* form synapses on contact
* retract if nothing happens

Simulation:
Each axon tip has multiple **random exploratory points.**

---

# **III. Dendrite-level mechanics (receiver behaviors)**

## **13. Dendritic branching**

Dendrites sprout new branches when neuron receives diverse or interesting input.

---

## **14. Dendritic spine motility (wiggling)**

Spines move, stretch, explore for new synapses.

Perfect for your dynamic-space grid.

**Rule:**
Spines randomly shift position within a radius each tick.

---

## **15. Branch strengthening (activity-based growth)**

If a particular input region is stimulating → dendrite grows toward it.

---

## **16. Dendritic retraction**

Unused dendritic branches shrink.

---

## **17. Dendritic filtering**

Dendrites are not just wires — they distort/shrink signals based on location.

You can simulate:

* proximal synapses stronger
* distal synapses weaker
* or introduce delay

---

# **IV. Neuron-level mechanics (cell behaviors)**

## **18. Leak (charge leakage)**

Neuron’s internal charge naturally drains over time.

---

## **19. Refractory period**

After firing, neuron is “tired” and cannot fire for some ticks.

---

## **20. Threshold adaptation**

If neuron fires too much → threshold rises
If too little → threshold lowers

This is a local homeostasis.

---

## **21. Global homeostasis**

Your idea: keep 20% of neurons active.

This mirrors biologically real **homeostatic plasticity**.

---

## **22. Intrinsic excitability changes**

Neuron can adjust its own firing tendency based on history.

**Rule:**
`exc += learning_rate * (target_rate - local_rate)`

---

## **23. Neuron drift (physical movement)**

Neurons can move on the sheet.

You can include:

* random Brownian drift
* attraction to certain stimuli
* repulsion from overcrowded regions

Creates organic structures.

---

## **24. Neuron death / apoptosis**

Occasionally, extremely quiet neurons die.

Optional, but fun.

---

## **25. Neurogenesis (birth of new neurons)**

Network can spawn new neurons in underpopulated regions.

---

# **V. Global / chemical / “mood” mechanics**

## **26. Neuromodulators**

Slow global signals that shift:

* thresholds
* weights
* plasticity rates

Examples:

* dopamine (reward)
* serotonin (stability/patience)
* acetylcholine (learning mode)

You can implement as:
`global_mode = slowly varying float that changes rules`

---

## **27. Diffusing activity field**

A chemical concentration that diffuses over time.

Neurons are attracted/repelled by it.

Gives you emergent waves and patterns.

---

## **28. Oscillatory global rhythms**

A slow global clock (like alpha/beta waves) modulates thresholds or leak.

---

## **29. Fatigue / “tired brain”**

After global spikes or external stimulation → everything becomes less excitable temporarily.

---

## **30. Recovery / “rest mode”**

Low activity → network becomes more excitable again.

---

# **VI. Signal mechanics**

## **31. Signal conduction delay (distance-based)**

Longer paths → slower arrival.

---

## **32. Spike amplitude variation**

Use binary or analog spikes.

---

## **33. Burst firing**

Some neurons fire multiple spikes in a rapid burst.

---

## **34. Background noise**

Low-level spontaneous firing creates exploration.

---

## **35. Lateral inhibition**

Inhibitory neurons suppress neighbors, improves contrast & pattern formation.

---

# **Weights: Are they on axons or dendrites?**

Biologically:

* Synaptic strength is **a property of the synapse**, not just axon or dendrite.
* But in simulation you can attach it to either side.

Best representation:

**Synapse object:**

* `pre_neuron`
* `post_neuron`
* `weight`
* `position_on_dendrite`
* `position_on_axon`
* `delay`

If the axon moves, the synapse moves with the axon branch.

If the dendrite moves, same thing.

Synapse breaks if distance > max.

---

# **If you want, I can next build:**

* a minimal simulation skeleton
* or an explicit data structure for neurons, dendrites, axons, synapses
* or rules for axon “hair” growth
* or a sequence of experiments to see emergent dynamics

What’s next sir dude?
