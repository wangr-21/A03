.operation-buttons {
  display: flex;
  align-items: center;
  gap: 12px;
}

.operation-button {
  padding: 4px 8px;
  font-size: 16px;
  color: var(--el-text-color-regular);
  cursor: pointer;
  transition: color 0.3s;
}

.operation-button:hover {
  color: var(--el-color-primary);
}

.operation-button.delete:hover {
  color: var(--el-color-danger);
} 