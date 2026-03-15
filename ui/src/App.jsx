import { useState, useEffect, useCallback, useRef } from 'react';
import {
  ReactFlow,
  Controls,
  Background,
  applyNodeChanges,
  applyEdgeChanges,
  MarkerType,
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';
import { getLayoutedElements } from './layout';
import SpecNode from './SpecNode';
import NodeDetails from './NodeDetails';
import './index.css';

const nodeTypes = { spec: SpecNode };

export default function App() {
  const [nodes, setNodes] = useState([]);
  const [edges, setEdges] = useState([]);
  const [selectedNodeData, setSelectedNodeData] = useState(null);
  const [error, setError] = useState(null);

  const BASE_POLL_MS = 5000;
  const MAX_POLL_MS = 30000;
  const backoffRef = useRef(BASE_POLL_MS);

  useEffect(() => {
    let isMounted = true;
    let timer;

    const fetchGraph = async () => {
      try {
        const res = await fetch('/api/graph');
        if (!res.ok) throw new Error('API Error');
        const data = await res.json();

        if (!isMounted) return;

        const flowNodes = data.nodes.map(n => ({
          id: n.id,
          type: 'spec',
          position: { x: 0, y: 0 },
          data: { ...n },
        }));

        const flowEdges = data.edges.map(e => ({
          id: `${e.source}-${e.target}`,
          source: e.source,
          target: e.target,
          type: 'smoothstep',
          animated: true,
          markerEnd: {
            type: MarkerType.ArrowClosed,
            width: 20,
            height: 20,
            color: '#4B5563',
          },
          style: { stroke: '#4B5563', strokeWidth: 2 },
        }));

        const { nodes: layoutedNodes, edges: layoutedEdges } = getLayoutedElements(
          flowNodes,
          flowEdges
        );

        setNodes(layoutedNodes);
        setEdges(layoutedEdges);
        setError(null);
        backoffRef.current = BASE_POLL_MS;
      } catch (e) {
        if (isMounted) {
          setError(e.message);
          backoffRef.current = Math.min(backoffRef.current * 2, MAX_POLL_MS);
        }
      }

      if (isMounted) {
        timer = setTimeout(fetchGraph, backoffRef.current);
      }
    };

    fetchGraph();

    return () => {
      isMounted = false;
      clearTimeout(timer);
    };
  }, []);

  const onNodesChange = useCallback(
    (changes) => setNodes((nds) => applyNodeChanges(changes, nds)),
    []
  );
  const onEdgesChange = useCallback(
    (changes) => setEdges((eds) => applyEdgeChanges(changes, eds)),
    []
  );

  const onNodeClick = useCallback((event, node) => {
    setSelectedNodeData(node.data);
  }, []);

  const onPaneClick = useCallback(() => {
    setSelectedNodeData(null);
  }, []);

  return (
    <div className="app-container">
      <header className="app-header">
        <div className="header-content">
          <div className="header-logo">
            <h1>Specdiff</h1>
            <span className="badge">Graph</span>
          </div>
          {error && <span className="error-badge">Disconnected</span>}
        </div>
      </header>

      <main className="graph-container">
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          onNodeClick={onNodeClick}
          onPaneClick={onPaneClick}
          nodeTypes={nodeTypes}
          fitView
          attributionPosition="bottom-right"
          minZoom={0.1}
        >
          <Background color="#1f2937" gap={24} size={2} />
          <Controls className="custom-controls" />
        </ReactFlow>

        {selectedNodeData && (
          <NodeDetails 
            data={selectedNodeData} 
            onClose={() => setSelectedNodeData(null)} 
          />
        )}
      </main>
    </div>
  );
}
