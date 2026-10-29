---
name: model-training
description: "Train, fit, or fine-tune a machine learning model (classifier, regressor, neural network, text or image model) on a dataset: stratified train/validation/test split, preprocessing pipeline, training with validation and early stopping, held-out evaluation, checkpointing, and saving or exporting the model. Use for any request to train a model, even a small one such as a scikit-learn classifier on iris, and for fine-tuning with PyTorch, TensorFlow/Keras, XGBoost, LightGBM, or Hugging Face. Not for exploratory data analysis notebooks (jupyter-notebook), debugging a crash or traceback (python-advanced-debugger), or deploying a model."
version: 1.0.0
author: Pixis
license: MIT
platforms: [linux, macos, windows]
metadata:
  pixis:
    category: Data Science
    tags: [machine-learning, training, pytorch, tensorflow, scikit-learn, fine-tuning]
    related_skills: [jupyter-notebook, python-advanced-debugger, test-first]
---

# Model training

Run the full training lifecycle on structured or unstructured data: load and preprocess, define the model, configure the optimizer and loss, train with validation and learning-rate scheduling, then checkpoint and export. Works for classical ML and deep learning.

## Inputs to get

The dataset location, the target variable or task, and any constraints (framework preference, compute budget, target metric). If one of these is missing and cannot be inferred, ask. Return a trained model artifact plus evaluation metrics.

## Workflow

1. **Load and inspect.** Read the data (disk, database, or remote storage). Profile feature distributions, class balance, missing values, and types. Split into train, validation, and test sets, stratified when classes are imbalanced.
2. **Preprocess.** Normalize or standardize, tokenize text, or augment images. Build reproducible, serializable pipelines so the same transforms run at inference.
3. **Define the model.** Classical: gradient boosting, SVMs, and so on. Deep learning: layers, activations, and regularization (dropout, weight decay). Use a pre-trained backbone with a task head when transfer learning applies.
4. **Configure training.** Choose the optimizer (Adam, SGD, AdamW), loss (cross-entropy, MSE, focal), learning-rate schedule (cosine annealing, step decay, warmup), and batch size. On GPUs enable mixed precision (`torch.amp`, `tf.keras.mixed_precision`) to save memory and speed up training.
5. **Train with validation.** Run the epochs, log loss and metrics per batch or epoch, evaluate on the validation set regularly, and use early stopping when validation performance plateaus for a set patience.
6. **Checkpoint and export.** Save the best-validation checkpoint and periodic ones. Export a portable format (ONNX, TorchScript, SavedModel). Log hyperparameters and metrics to an experiment tracker.

## Supported technologies

- **Frameworks:** PyTorch, TensorFlow/Keras, scikit-learn, XGBoost, LightGBM
- **Distributed:** PyTorch DDP, Horovod, TensorFlow MirroredStrategy
- **Tracking:** MLflow, Weights & Biases, TensorBoard
- **Data loading:** PyTorch DataLoader, tf.data, pandas, Hugging Face Datasets

## Pattern: PyTorch loop with early stopping

```python
optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3, weight_decay=1e-2)
scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs)
criterion = nn.CrossEntropyLoss()
best, patience, bad = 0.0, 3, 0
for epoch in range(epochs):
    model.train()
    for xb, yb in train_loader:
        xb, yb = xb.to(device), yb.to(device)
        loss = criterion(model(xb), yb)
        optimizer.zero_grad(); loss.backward(); optimizer.step()
    scheduler.step()

    model.eval(); correct = total = 0
    with torch.no_grad():
        for xb, yb in val_loader:
            xb, yb = xb.to(device), yb.to(device)
            correct += (model(xb).argmax(1) == yb).sum().item(); total += yb.size(0)
    val_acc = correct / total
    if val_acc > best:
        best, bad = val_acc, 0
        torch.save(model.state_dict(), "best_model.pt")
    else:
        bad += 1
        if bad >= patience: break
```

Split first with `train_test_split(..., stratify=y, random_state=42)`.

## Pattern: fine-tune with Hugging Face

Load the dataset and tokenizer, tokenize with `padding="max_length"`, `truncation=True`, load `AutoModelForSequenceClassification`, then:

```python
args = TrainingArguments(output_dir="./results", num_train_epochs=3,
    per_device_train_batch_size=16, per_device_eval_batch_size=32,
    eval_strategy="epoch", save_strategy="epoch", load_best_model_at_end=True,
    metric_for_best_model="f1", fp16=True, learning_rate=2e-5,
    weight_decay=0.01, warmup_steps=500, logging_steps=100)
trainer = Trainer(model=model, args=args, train_dataset=train_ds,
                  eval_dataset=eval_ds, compute_metrics=compute_metrics)
trainer.train(); trainer.save_model("./best_model")
```

Use `compute_metrics` returning accuracy and F1 (scikit-learn). Set `fp16` only when a GPU is available.

## Best practices

- Stratify splits on imbalanced data so each split reflects the true class distribution.
- Use learning-rate warmup when fine-tuning pre-trained models, to avoid catastrophic forgetting early on.
- Enable mixed precision (`fp16` or `bf16`) on GPUs; it roughly halves memory and speeds training.
- Log everything: hyperparameters, per-epoch metrics, system resource usage, and the git hash of the training code.
- Save checkpoints often and always keep the best-validation one, so crashes or overtraining do not cost progress.
- Evaluate on a held-out set that was never used for training or hyperparameter choice, for an unbiased generalization estimate.

## Edge cases

- **Small datasets (under about 1,000 samples):** use k-fold cross-validation instead of one split; prefer transfer learning or pre-trained models over training from scratch.
- **Extreme imbalance (over 100:1):** oversample (SMOTE), use class-weighted or focal loss, and judge by F1, precision-recall AUC, or Matthews correlation, not accuracy.
- **Divergence or NaN loss:** lower the learning rate, clip gradients (`torch.nn.utils.clip_grad_norm_`), check for infinite values in the data, or turn off mixed precision to rule out numerical instability.
- **Out of memory:** reduce batch size, use gradient accumulation or mixed precision, or enable gradient checkpointing to trade compute for memory.
- **Non-stationary data (concept drift):** retrain periodically on fresh data, split by time instead of randomly, and watch production metrics for degradation.

## Completion criteria

- Splits were made (stratified where needed) and the test set was not used for tuning.
- Preprocessing is saved or reproducible so inference uses identical transforms.
- Training was validated each epoch; the best checkpoint was saved and the model exported.
- Hyperparameters, metrics, and the code version were logged.
- The final report states the metrics on held-out data, the framework and settings, and any caveats (small data, imbalance, instability).
