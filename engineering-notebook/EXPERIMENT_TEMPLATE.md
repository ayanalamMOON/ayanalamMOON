# Engineering Experiment Template

Use this template for investigations where you want the result to be reproducible and technically defensible. The automated profile feed records commits, not experimental conclusions; only publish measurements after actually running the experiment.

## Title

A specific question, algorithm, system, or optimization being investigated.

## Problem and motivation

What problem is being addressed, why does it matter, and what is the current baseline?

## Hypothesis

State a falsifiable prediction.

## Setup

- Repository and commit:
- Hardware and operating system:
- Runtime, compiler, and dependency versions:
- Dataset or input dimensions:
- Configuration and random seed:

## Method

List the steps needed to reproduce the test. Identify the baseline and the single variable being changed.

## Correctness checks

Describe reference outputs, invariants, acceptable numerical tolerance, or test cases used to establish correctness.

## Metrics

Specify metrics before running the experiment, including units, warm-up policy, sample count, and summary statistics.

## Results

Record raw measurements or link a machine-readable result file. Include negative and inconclusive results.

## Interpretation

Explain what the results support, what they do not establish, and plausible alternative explanations.

## Limitations and follow-up

Document threats to validity, platform dependence, and the next experiment.

## Reproduction command

Provide the exact commands or workflow link needed to reproduce the result.
