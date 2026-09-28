---
layout: post
title: "The Enterprise AI Blueprint: MLOps, LLMOps, Disaggregated Serving, Infrastructure, and Governance"
date: 2026-09-28
author: Namit Sehgal
excerpt: "Executive Summary Building enterprise AI isn't just about calling an API or spinning up a GPU. When scaling AI across enterprise infrastructure, standard web architecture breaks down. Traditional load"
hashnode_url: https://articles.namitsehgal.com/the-enterprise-ai-blueprint-mlops-llmops-disaggregated-serving-infrastructure-and-governance
---

## Executive Summary

Building enterprise AI isn't just about calling an API or spinning up a GPU. When scaling AI across enterprise infrastructure, standard web architecture breaks down. Traditional load balancers treat AI requests like basic web traffic, leading to **high latencies, GPU memory bottlenecks, and skyrocketing operational costs**.

This blueprint outlines how to run modern AI efficiently on enterprise infrastructure:

1. **Unified AI Infrastructure & Hybrid Routing:** Architecting an Enterprise Model Gateway to route dynamically between self-hosted clusters and proprietary foundation APIs (e.g., Google Gemini, OpenAI GPT, Anthropic Claude).
2. **End-to-End MLOps vs. LLMOps Pipelines:** Automating the lifecycle of classical predictive ML, open-weight Generative AI, and managed SaaS endpoints.
3. **General vs. Domain-Specific Models:** Architectural trade-offs between massive foundation models and focused, on-premise domain models.
4. **Modern LLMOps (**`llm-d`**):** Decoupling prompt processing from token generation to maximize self-hosted GPU performance.
5. **Kubernetes Infrastructure with Gateway API:** Production manifests for `llm-d` using the Gateway API Inference Extension (`inference.networking.k8s.io/v1`).
6. **ML Evaluation Metrics & Infrastructure Impact:** How Recall, Precision, F1-Score, and Loss correlate directly with VRAM allocations, KV-cache routing, and replica scaling.
7. **Air-Gapped Governance & Code Demonstrations:** Dynamic routing sidecars, inline policy enforcement, ONNX CPU execution, and OpenVINO quantization.

## 1. Proprietary Model Integration & The Unified Enterprise Gateway

A common question when designing AI infrastructure is: **Where do commercial foundation models like Google Gemini fit?**

Commercial model providers do not distribute raw weights for private Kubernetes hosting. Instead, vendor platforms manage the underlying GPU clusters, KV-cache strategies, and Prefill/Decode disaggregation behind managed APIs or enterprise cloud endpoints (such as Google Cloud Vertex AI via Private Service Connect).

To handle both worlds, modern enterprise architecture deploys a **Unified API Gateway Abstraction** that unifies self-hosted open-weight infrastructure with proprietary SaaS models under a single control plane.

![](https://cdn.hashnode.com/uploads/covers/6a157ef2da253d50d4a02fc4/7a48cc54-daff-4671-9645-a429655df25d.png)

### Self-Hosted vs. Proprietary Architectural Trade-Offs

| Dimension | Self-Hosted / Open-Weight Models (`llm-d`) | Proprietary Models (Gemini, Claude, GPT) |
| --- | --- | --- |
| **Model Weights** | Direct access; stored in private GCS/S3 buckets or local NVMe. | Proprietary black box; accessed strictly via authenticated TLS/REST endpoints. |
| **Infrastructure Control** | Custom Kubernetes clusters, `llm-d` routing, GPU VRAM, and Triton/vLLM engines. | Vendor-managed capacity, Provisioned Throughput, or dedicated tenant instances. |
| **Prefill / Decode Split** | Handled natively by your infra engineers via RDMA / PagedAttention pools. | Handled internally by vendor serving infrastructure. |
| **Data Privacy & Air-Gap** | **Fully Air-Gapped:** Operates offline in private data centers or sovereign cloud enclaves. | **Managed Boundary:** Secured using VPC Service Controls, Private Service Connect, or enterprise DPAs. |
| **Cost & Sizing Model** | Fixed GPU operational expense (OpEx/CapEx); cost per token approaches zero at high utilization. | Variable pay-per-token or allocated Query-Per-Second (QPS) reservation fees. |

## 2. MLOps vs. LLMOps Pipelines Explained

To build a complete enterprise AI platform, you must understand how classical ML, self-hosted LLMs, and proprietary SaaS models differ across their operational lifecycles.

### Data Flow Architecture

![](https://cdn.hashnode.com/uploads/covers/6a157ef2da253d50d4a02fc4/2d7145f3-d30d-4f94-8e07-442c1e570789.png)

### Classical MLOps Pipeline

Designed for **structured data** where output is deterministic (e.g., credit scoring, fraud detection, tabular predictions):

1. **Data Ingestion & Feature Store:** Raw transactional data is cleaned and stored in a feature store (e.g., Feast) to ensure training and serving use identical data representations.
2. **Model Training:** Algorithms (XGBoost, LightGBM, Random Forest, Scikit-learn) are trained on tabular datasets.
3. **Model Registry:** Model binaries are versioned alongside dataset metadata in tools like MLflow.
4. **Compilation & Optimization:** The model is converted to **ONNX (Open Neural Network Exchange)** format for high-speed CPU execution.
5. **Inference & Monitoring:** Served via engines like **Triton Inference Server** running on multi-threaded CPUs, monitored for data drift and accuracy decay.

### Modern Self-Hosted LLMOps Pipeline

Designed for **unstructured data** where output is non-deterministic and context-driven, requiring local infrastructure ownership:

1. **Data & Knowledge Ingestion:** Unstructured documents are processed, embedded, and stored in vector databases (e.g., Milvus, Qdrant) or Knowledge Graphs for Retrieval-Augmented Generation (RAG).
2. **Model Adaptation (PEFT / LoRA):** Open-weight base models are adapted using parameter-efficient fine-tuning (LoRA) on enterprise-specific datasets.
3. **Prompt & Chain Registry:** Prompt templates, system instructions, and RAG pipelines are versioned as code alongside model weights.
4. **Disaggregated Serving (**`llm-d`**):** Models are deployed across specialized GPU clusters using KV-cache-aware gateways to handle high-throughput token generation.
5. **Runtime Governance & Evaluation:** Every response is checked in real time for PII leakage, hallucination scores, and policy compliance before reaching the user.

### Managed SaaS Pipeline (e.g., Gemini)

Designed for **massive scale, multimodal inputs, and ultra-complex reasoning** where hosting host-level GPUs is unfeasible:

1. **Managed Knowledge Context:** Enterprise data feeds directly into managed vector search indices or document databases via private cloud connectors.
2. **Adapter & Parameter Tuning:** Uses vendor-managed tuning workflows (e.g., Vertex AI SFT/LoRA tuning) that return lightweight adapter references rather than raw binary checkpoints.
3. **Managed Endpoint Provisioning:** Capacity is reserved using Provisioned Throughput or dedicated project quotas to guarantee latency SLAs during demand spikes.
4. **Unified Gateway Governance:** Enforces corporate compliance policies, audit logs, and cost controls prior to outbound API calls.

## 3. Custom General AI Models vs. Domain-Specific Custom Models

When architecting AI systems, a critical decision is whether to deploy a **Custom General Model** (self-hosted or proprietary SaaS) or a **Domain-Specific Custom Model**.

![](https://cdn.hashnode.com/uploads/covers/6a157ef2da253d50d4a02fc4/461e9388-6d4f-48f7-b26b-0c7bd5d4ad18.png)

### 1. Custom General AI Model

* **Definition:** A large foundation model deployed either on private infrastructure or via enterprise managed endpoints (e.g., Gemini 1.5 Pro) with custom system prompts, vector RAG pipelines, and multi-tool routing.
* **When to use:** Multi-purpose assistant platforms, complex code generation, open-ended reasoning, or broad document analysis across diverse departments.
* **Infrastructure Requirements:** Either multi-GPU clusters running `llm-d` with Prefill/Decode disaggregation or secure managed SaaS API endpoints connected over Private Service Connect.

### 2. Domain-Specific Custom Model

* **Definition:** A smaller base model (1B–14B parameters) fine-tuned (e.g., via LoRA) on highly specialized, private domain data (such as trade settlement rules, credit underwriting policies, or internal IT logs).
* **When to use:** High-volume, narrow tasks where low latency, low cost, and strict deterministic accuracy are critical (e.g., extraction of structured fields from financial SWIFT messages).
* **Infrastructure Requirements:** Asymmetric CPU scale-out clusters running **vLLM-CPU** or **OpenVINO GenAI**, eliminating GPU dependencies for serving while using transient GPU pools solely for fine-tuning.

## 4. Dynamic Resource Allocation & Disaggregated Serving (`llm-d`)

### The Problem with Traditional Serving

An LLM generates text in two distinct, mathematically different phases:

![](https://cdn.hashnode.com/uploads/covers/6a157ef2da253d50d4a02fc4/aeab4de0-a844-4863-a9eb-f6c6d9517a53.png)

When a standard load balancer forces one GPU to handle both phases, the GPU becomes memory-starved during the writing phase, creating massive tail latencies for all users.

### The Solution: `llm-d` Architecture

![](https://cdn.hashnode.com/uploads/covers/6a157ef2da253d50d4a02fc4/60611d9a-8a92-4ae1-a12a-c8f7798165a1.png)

1. **Prefix-Aware Routing:** `llm-d` checks which GPU pod already holds the cached system prompt or document context. If a match exists, it routes the request there, skipping redundant compute and dropping **Time-to-First-Token (TTFT) by up to 16x**.
2. **Prefill/Decode (P/D) Disaggregation:** Prefill nodes process the prompt rapidly, then transfer the calculated KV-cache directly to Decode nodes via high-speed GPU-to-GPU RDMA networks without touching host CPU memory.
3. **Tiered KV-Caching:** If GPU VRAM fills up, `llm-d` offloads inactive KV-cache blocks to system host RAM (DRAM) or local NVMe storage, preventing severe recalculation penalties when processing long documents.

## 5. Production Kubernetes Infrastructure Specs (`llm-d` + Gateway API)

The following production-ready manifests show how to deploy `llm-d` on Kubernetes using the official **Kubernetes Gateway API Inference Extension** (`inference.networking.k8s.io/v1`).

![](https://cdn.hashnode.com/uploads/covers/6a157ef2da253d50d4a02fc4/2b194327-f2ad-435a-9e34-b37d6457ded7.png)

### 1. Gateway API & Ingress Route

```
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: llm-d-gateway
  namespace: llm-serving
spec:
  gatewayClassName: agentgateway
  listeners:
  - name: http
    port: 80
    protocol: HTTP
    allowedRoutes:
      namespaces:
        from: Same
---
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: llama-3-route
  namespace: llm-serving
spec:
  parentRefs:
  - name: llm-d-gateway
  hostnames:
  - "ai-api.internal.domain"
  rules:
  - matches:
    - path:
        type: PathPrefix
        value: /v1/chat/completions
    backendRefs:
    - group: inference.networking.k8s.io
      kind: InferencePool
      name: vllm-llama3-70b-pool
      port: 8000
```

### 2. Gateway API Inference Extension (`InferencePool`)

```
apiVersion: inference.networking.k8s.io/v1
kind: InferencePool
metadata:
  name: vllm-llama3-70b-pool
  namespace: llm-serving
  labels:
    model.llm-d.ai/name: meta-llama-3.3-70b
spec:
  selector:
    app: vllm-llama3-70b
    role: model-server
  targetPorts:
  - number: 8000
  endpointPickerRef:
    group: ""
    kind: Service
    name: llama3-70b-epp-service
    port:
      number: 9002
  failureMode: FailOpen
```

### 3. `llm-d` Endpoint Policy Provider (EPP / Router)

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: llama3-70b-epp
  namespace: llm-serving
  labels:
    app.kubernetes.io/component: endpoint-picker
spec:
  replicas: 2
  selector:
    matchLabels:
      app: llama3-70b-epp
  template:
    metadata:
      labels:
        app: llama3-70b-epp
    spec:
      containers:
      - name: epp-router
        image: ghcr.io/llm-d/llm-d-routing-sidecar:v0.9.0
        ports:
        - name: ext-proc
          containerPort: 9002
        - name: metrics
          containerPort: 9090
        env:
        - name: INFERENCE_POOL_NAME
          value: "vllm-llama3-70b-pool"
        - name: NAMESPACE
          valueFrom:
            fieldRef:
              fieldPath: metadata.namespace
        - name: ENABLE_PREFIX_AWARE_ROUTING
          value: "true"
        - name: KV_CACHE_DECAY_FACTOR
          value: "0.85"
        resources:
          limits:
            cpu: "2"
            memory: 2Gi
          requests:
            cpu: "500m"
            memory: 512Mi
---
apiVersion: v1
kind: Service
metadata:
  name: llama3-70b-epp-service
  namespace: llm-serving
spec:
  selector:
    app: llama3-70b-epp
  ports:
  - name: ext-proc
    port: 9002
    targetPort: 9002
```

### 4. Target Model Server Deployment (vLLM Engine)

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: vllm-llama3-70b
  namespace: llm-serving
spec:
  replicas: 4
  selector:
    matchLabels:
      app: vllm-llama3-70b
      role: model-server
  template:
    metadata:
      labels:
        app: vllm-llama3-70b
        role: model-server
    spec:
      containers:
      - name: vllm-container
        image: vllm/vllm-openai:v0.7.2
        args:
        - "--model"
        - "meta-llama/Llama-3.3-70B-Instruct"
        - "--tensor-parallel-size"
        - "4"
        - "--enable-prefix-caching"
        - "--host"
        - "0.0.0.0"
        - "--port"
        - "8000"
        ports:
        - containerPort: 8000
          name: http
        resources:
          limits:
            nvidia.com/gpu: "4"
            memory: 160Gi
          requests:
            nvidia.com/gpu: "4"
            memory: 128Gi
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 120
          periodSeconds: 10
```

## 6. ML Evaluation Metrics & Infrastructure Correlations

ML evaluation metrics dictate model training accuracy while directly influencing serving parameters such as VRAM allocation, context length limits, and routing logic in `llm-d`.

![](https://cdn.hashnode.com/uploads/covers/6a157ef2da253d50d4a02fc4/6160e92d-7ae8-4e6a-a0a8-80b7410313ec.png)

### Metric Definitions & Formulae

#### Precision & Recall

$$\text{Precision} = \frac{\text{True Positives (TP)}}{\text{True Positives (TP)} + \text{False Positives (FP)}}$$

$$\text{Recall} = \frac{\text{True Positives (TP)}}{\text{True Positives (TP)} + \text{False Negatives (FN)}}$$

* **Precision** measures exactness: out of all positive predictions, how many were correct?
* **Recall** measures completeness: out of all actual positive instances, how many did the system retrieve or generate?

#### F1-Score

$$\text{F1-Score} = 2 \times \frac{\text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}}$$

The harmonic mean balances Precision and Recall, proving vital when evaluating RAG pipelines, tool-calling agents, and structured outputs.

#### Training Loss & Evaluation Precision

$$\text{Training Loss (Cross-Entropy)} = -\frac{1}{N} \sum\_{i=1}^{N} \log P(y\_i \mid x\_i)$$

Training loss quantifies model error during pre-training or fine-tuning. **Evaluation Precision** evaluates token-level or task-level accuracy on a held-out test dataset to prevent overfitting.

## Mapping Machine Learning Metrics to Infrastructure Configurations

### 1. High Recall (RAG & Long Context)

* **ML Goal:** Process large retrieved contexts for maximum document coverage.
* **Infra Impact:** High VRAM KV-cache allocation; requires prefix cache reuse across pods.
* **Target Config:** --enable-prefix-caching ENABLE\_PREFIX\_AWARE\_ROUTING: "true"

### 2. High Precision (Tool Call & Structured Output)

* **ML Goal:** Deterministic token generation, low temperature, and exact schema compliance.
* **Infra Impact:** LoRA adapter VRAM overhead and strict memory ceilings per inference pod.
* **Target Config:** resources: limits: [nvidia.com/gpu](https://www.google.com/search?q=https%3A%2F%2Fnvidia.com%2Fgpu): "4"

### 3. Low Loss / High Eval Precision

* **ML Goal:** High token certainty, producing concise and efficient generation sequences.
* **Infra Impact:** Shorter generation times, reduced GPU dwell time, higher cluster throughput.
* **Target Config:** EPP\_SCHEDULER\_POLICY="KV\_CACHE\_DECAY\_FACTOR"

### 4. High F1-Score (Balanced Production Pipeline)

* **ML Goal:** Optimal balance between response accuracy and generation latency.
* **Infra Impact:** Dynamic pod scaling and request routing tuned for Target Time-To-First-Token (TTFT).
* **Target Config:** kind: InferencePool spec: replicas: 4

## 7. Code Examples

### Example 1: Unified Enterprise API Gateway (Hybrid Router Python Script)

This production script acts as the Unified Gateway. It evaluates request metadata, checks data sensitivity, inspects prompt length, and dynamically routes traffic between self-hosted `llm-d` clusters and commercial cloud APIs (e.g., Google Gemini on Vertex AI).

```
import os
import requests
from typing import Dict, Any

class EnterpriseUnifiedGateway:
    """
    Unified API Gateway: Dynamically routes incoming enterprise requests
    between private self-hosted llm-d clusters and proprietary APIs (e.g., Gemini).
    """
    def __init__(self):
        self.llm_d_cluster_url = os.getenv("LLM_D_GATEWAY_URL", "http://ai-api.internal.domain/v1/chat/completions")
        self.gemini_api_key = os.getenv("GEMINI_API_KEY", "mock-gemini-key")
        self.gemini_endpoint = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent"

    def route_request(self, payload: Dict[str, Any], is_confidential: bool = False) -> Dict[str, Any]:
        prompt = payload.get("prompt", "")
        token_estimate = len(prompt.split()) * 1.3
        
        # Rule 1: Air-Gapped / Strictly Confidential Data -> Direct to Private llm-d
        if is_confidential:
            print(" Routing to Private llm-d Cluster (Strict Data Confidentiality Policy Enforced)")
            return self._call_llm_d_cluster(payload)
            
        # Rule 2: Ultra-Long Context / Complex Reasoning -> Route to Proprietary API (Gemini)
        if token_estimate > 32000 or payload.get("require_multimodal", False):
            print(" Routing to Google Gemini API (High-Capacity Context / Multimodal Task)")
            return self._call_gemini_api(prompt)

        # Rule 3: Standard High-Volume Workload -> Private llm-d Cluster for Low Token Cost
        print(" Routing to Private llm-d Cluster (Optimized Unit Cost / Low Latency)")
        return self._call_llm_d_cluster(payload)

    def _call_llm_d_cluster(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        try:
            # Internal request sent via Kubernetes InferencePool Gateway
            response = requests.post(self.llm_d_cluster_url, json=payload, timeout=30)
            return response.json()
        except Exception as e:
            return {"status": "error", "source": "llm-d-cluster", "message": str(e)}

    def _call_gemini_api(self, prompt: str) -> Dict[str, Any]:
        headers = {"Content-Type": "application/json"}
        params = {"key": self.gemini_api_key}
        data = {"contents": [{"parts": [{"text": prompt}]}]}
        try:
            # External secure request to Gemini endpoint
            response = requests.post(self.gemini_endpoint, headers=headers, params=params, json=data, timeout=30)
            return {"status": "success", "source": "gemini-api", "data": response.json()}
        except Exception as e:
            return {"status": "error", "source": "gemini-api", "message": str(e)}

# Usage Example
if __name__ == "__main__":
    gateway = EnterpriseUnifiedGateway()
    
    # Example A: Sensitive HR document extraction -> Forced to On-Prem / Private Cluster
    res_a = gateway.route_request({"prompt": "Extract salary history for ID 9921"}, is_confidential=True)
    
    # Example B: Massive multi-page document summary -> Routed to Gemini
    large_doc_prompt = "Analyze this balance sheet context: " + ("data " * 35000)
    res_b = gateway.route_request({"prompt": large_doc_prompt}, is_confidential=False)
```

### Example 2: Classical MLOps — High-Speed CPU Serving with Triton & ONNX Runtime (Python)

This example shows how a custom credit risk model is exported to ONNX format and executed on a multi-threaded CPU runtime for sub-millisecond predictions.

```
import numpy as np
import onnxruntime as ort

class CreditRiskInferenceEngine:
    """
    Classical MLOps Serving Engine: Executes a trained XGBoost credit risk model
    compiled to ONNX format using multi-threaded CPU execution.
    """
    def __init__(self, model_path: str):
        # Configure thread pooling for high-throughput CPU inference
        self.opts = ort.SessionOptions()
        self.opts.intra_op_num_threads = 4  # Compute thread count
        self.opts.inter_op_num_threads = 2  # Concurrent request thread count
        self.opts.execution_mode = ort.ExecutionMode.ORT_PARALLEL
        self.opts.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
        
        # Load compiled ONNX model
        self.session = ort.InferenceSession(model_path, self.opts, providers=['CPUExecutionProvider'])
        self.input_name = self.session.get_inputs()[0].name
        self.output_name = self.session.get_outputs()[0].name

    def predict_risk_score(self, feature_vector: list) -> dict:
        """
        Accepts raw financial metrics: [debt_ratio, credit_utilization, income, late_payments]
        Returns credit default probability in sub-milliseconds.
        """
        input_data = np.array([feature_vector], dtype=np.float32)
        raw_outputs = self.session.run([self.output_name], {self.input_name: input_data})
        
        default_probability = float(raw_outputs[0][0][1])
        return {
            "default_probability": round(default_probability, 4),
            "approved": default_probability < 0.15
        }

# Usage Example
if __name__ == "__main__":
    applicant_features = [0.28, 0.42, 125000.0, 0.0]
    # engine = CreditRiskInferenceEngine("models/credit_risk_v2.onnx")
    print("Classical MLOps Engine initialized for sub-millisecond CPU execution.")
```

### Example 3: Domain-Specific LLMOps — Asymmetric CPU Inference with OpenVINO GenAI (Python)

This example demonstrates serving a fine-tuned 7B parameter Small Language Model (SLM) on standard enterprise CPU hardware using optimized vectorization (AVX-512/AMX) and **PagedAttention** directly in system DRAM.

```
import time
from openvino_genai import LLMPipeline, GenerationConfig

class OnPremDomainSLMEngine:
    """
    Domain-Specific LLMOps Engine: Runs a fine-tuned domain model (INT4 quantized)
    on standard x86 CPU hardware without GPU requirements.
    """
    def __init__(self, model_dir: str):
        print("Loading quantized domain model into system DRAM...")
        self.pipe = LLMPipeline(model_dir, "CPU")
        
    def generate_domain_response(self, prompt: str, system_context: str) -> str:
        formatted_prompt = f"<|system|>\n{system_context}\n<|user|>\n{prompt}\n<|assistant|>\n"
        
        config = GenerationConfig()
        config.max_new_tokens = 256
        config.temperature = 0.1  # Low temperature for deterministic domain output
        config.top_p = 0.9
        
        start_time = time.time()
        output = self.pipe.generate(formatted_prompt, config)
        latency = time.time() - start_time
        
        print(f"Inference completed in {latency:.2f}s using CPU DRAM PagedAttention.")
        return output

# Usage Example
if __name__ == "__main__":
    system_instruction = "You are a regulatory compliance engine for trade settlement."
    user_query = "What is the settlement cycle rule for UK equities?"
    # engine = OnPremDomainSLMEngine("models/trade_compliance_slm_int4")
    print("Domain-Specific SLM Engine ready for CPU-native execution.")
```

### Example 4: Air-Gapped Governance — SAFR Runtime Policy Sidecar (Python)

This example implements an inline policy engine that evaluates proposed model actions, detects PII, and assigns a **Disposition Envelope** (`AUTO_EXECUTE`, `DENY`, or `ESCALATE`) before execution.

```
import re
import uuid
from enum import Enum
from typing import Dict, Any

class Disposition(Enum):
    AUTO_EXECUTE = "AUTO_EXECUTE"  # Low-risk, read-only
    OBSERVE = "OBSERVE"            # Allowed, logged for auditing
    DENY = "DENY"                  # Security/PII policy violation
    ESCALATE = "ESCALATE"          # High-risk state mutation -> HITL Required

class SAFRGovernanceSidecar:
    """
    Inline Policy Sidecar implementing the SAFR Governance Framework.
    Intercepts AI model output before tool call execution.
    """
    def __init__(self):
        self.pii_pattern = re.compile(r'\b(?:\d[ -]*?){13,16}\b')
        self.high_risk_actions = {"transfer_funds", "modify_credit_limit", "delete_account"}

    def inspect_and_evaluate(self, proposed_action: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        param_str = str(parameters)
        
        # 1. Check for PII / Data Privacy Violations
        if self.pii_pattern.search(param_str):
            return {
                "disposition": Disposition.DENY.value,
                "reason": "PII / Sensitive data detected in parameters.",
                "action": proposed_action
            }
        
        # 2. Check for High-Risk State Mutations -> Trigger Escalation Token
        if proposed_action in self.high_risk_actions:
            state_token = f"HITL-TOKEN-{uuid.uuid4().hex[:8].upper()}"
            return {
                "disposition": Disposition.ESCALATE.value,
                "reason": f"High-risk action '{proposed_action}' requires Human-in-the-Loop approval.",
                "hitl_state_token": state_token,
                "action": proposed_action,
                "parameters": parameters
            }
        
        # 3. Default to Auto-Execute for Safe Operations
        return {
            "disposition": Disposition.AUTO_EXECUTE.value,
            "reason": "Action complies with safety policy.",
            "action": proposed_action,
            "parameters": parameters
        }

# Usage Example
if __name__ == "__main__":
    governance = SAFRGovernanceSidecar()
    
    result_1 = governance.inspect_and_evaluate(
        proposed_action="transfer_funds",
        parameters={"amount": 50000, "destination_account": "ACC-992183"}
    )
    print("Action 1 Evaluation:", result_1)
    
    result_2 = governance.inspect_and_evaluate(
        proposed_action="lookup_customer",
        parameters={"query_credit_card": "4532-0112-9921-4410"}
    )
    print("Action 2 Evaluation:", result_2)
```

### Example 5: ML Evaluation Metric Calculator (Python)

This script computes Precision, Recall, F1-Score, and Cross-Entropy Loss on generation/classification logs, linking training evaluation directly to system observability.

```
import numpy as np

def compute_evaluation_metrics(y_true: list[int], y_pred: list[int], logits: list[float]) -> dict:
    """
    Calculates Precision, Recall, F1-Score, and Loss for model evaluations.
    """
    tp = sum(1 for gt, pred in zip(y_true, y_pred) if gt == 1 and pred == 1)
    fp = sum(1 for gt, pred in zip(y_true, y_pred) if gt == 0 and pred == 1)
    fn = sum(1 for gt, pred in zip(y_true, y_pred) if gt == 1 and pred == 0)

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1_score = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

    # Calculate Cross-Entropy Loss on predictions
    probs = 1 / (1 + np.exp(-np.array(logits)))
    targets = np.array(y_true)
    epsilon = 1e-15
    probs = np.clip(probs, epsilon, 1 - epsilon)
    training_eval_loss = -np.mean(targets * np.log(probs) + (1 - targets) * np.log(1 - probs))

    return {
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1_score": round(f1_score, 4),
        "eval_loss": round(float(training_eval_loss), 4)
    }

# Usage Example
if __name__ == "__main__":
    ground_truth = [1, 0, 1, 1, 0, 1, 0, 0, 1, 0]
    predictions  = [1, 0, 1, 0, 0, 1, 1, 0, 1, 0]
    raw_logits   = [2.5, -1.2, 1.8, -0.5, -2.0, 1.1, 0.8, -1.5, 2.2, -1.8]

    metrics = compute_evaluation_metrics(ground_truth, predictions, raw_logits)
    
    print("=== MODEL EVALUATION REPORT ===")
    print(f"Evaluation Precision : {metrics['precision']}")
    print(f"Evaluation Recall    : {metrics['recall']}")
    print(f"F1-Score             : {metrics['f1_score']}")
    print(f"Cross-Entropy Loss   : {metrics['eval_loss']}")
```

## 8. Comprehensive Architectural Summary Matrix

| Dimension | Classical MLOps | Custom General AI (Self-Hosted) | Custom General AI (Proprietary SaaS) | Domain-Specific Custom Model |
| --- | --- | --- | --- | --- |
| **Primary Workload** | Predictive analytics, tabular scoring, fraud detection. | High-volume internal tasks, sensitive data processing. | Massive context analysis, multimodal tasks, advanced reasoning. | Specialized domain tasks (e.g., trade settlement, policy extraction). |
| **Data Type** | Structured (Tables, Time-Series). | Unstructured (Internal Docs, Code base). | Unstructured (Enterprise BigQuery, Large Files). | Unstructured Domain Data (PDFs, Logs, Trade Messages). |
| **Serving Runtime** | **Triton Server** + **ONNX Runtime**. | `llm-d` Disaggregated Cluster (P/D Split). | Cloud Managed Endpoint (e.g., Google Vertex AI). | **vLLM-CPU** / **OpenVINO GenAI** (DRAM PagedAttention). |
| **Target Hardware** | Scale-out Enterprise CPUs. | Dedicated Multi-GPU Clusters (NVLink / HBM). | Vendor-Managed Infra / Dedicated Cloud Pods. | Enterprise CPUs (Serving) + Transient GPUs (Tuning). |
| **Kubernetes Control** | Standard `Deployment` + KEDA. | **Gateway API** + `InferencePool` + EPP Router. | Enterprise Unified Router / External Egress API. | CPU Deployment + Vectorized Memory Limits. |
| **Primary ML Metrics** | AUC-ROC, Precision, Recall, MSE. | Perplexity, TTFT, Token-level Precision. | Task Accuracy, Multimodal Recall, Benchmarks. | F1-Score, Structured Extraction Precision. |
| **Governance Engine** | Feature drift & accuracy monitoring. | `llm-d` Routing + SAFR Policy Sidecars. | Cloud IAM, VPC-SC, + SAFR Ingress Sidecars. | SAFR Policy Sidecars + Local MCP Connectors. |

## 9. Conclusion

Scaling enterprise AI requires moving beyond binary choices between pure cloud APIs or pure self-hosting. By establishing a **Unified API Gateway Abstraction layer**, organizations can seamlessly blend proprietary foundation platforms like **Google Gemini** with self-hosted open-weight clusters running `llm-d` **on Kubernetes**.

Decoupling compute phases through Prefill/Decode disaggregation, enforcing runtime policy sidecars, and right-sizing tasks between general and domain-specific engines ensures an enterprise AI architecture that is secure, resilient, cost-effective, and fully scalable.
