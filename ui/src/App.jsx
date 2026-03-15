import { useState, useEffect, useCallback, useMemo, useRef } from 'react';
import isEqual from 'lodash/isEqual';
import { AnimatePresence } from 'framer-motion';
import {
  ReactFlow,
  Controls,
  Background,
  MiniMap,
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
  const [hoveredNode, setHoveredNode] = useState(null);
  const [error, setError] = useState(null);
  const prevDataRef = useRef(null);

  // Use a ref polling interval to refresh the graph data every 2 seconds
  useEffect(() => {
    let isMounted = true;
    let timer;

    const fetchGraph = async () => {
      try {
        const res = await fetch('/api/graph');
        if (!res.ok) throw new Error('API Error');
        const data = await res.json();

        if (!isMounted) return;

        if (prevDataRef.current && isEqual(prevDataRef.current, data)) {
          return;
        }
        prevDataRef.current = data;

        // Map Backend Nodes -> React Flow Nodes
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

  const onNodeMouseEnter = useCallback((_, node) => setHoveredNode(node.id), []);
  const onNodeMouseLeave = useCallback(() => setHoveredNode(null), []);

  const highlightNodeId = hoveredNode || selectedNodeData?.id;

  const highlightedNodeIds = useMemo(() => {
    if (!highlightNodeId) return new Set();
    const connected = new Set([highlightNodeId]);
    edges.forEach(e => {
      if (e.source === highlightNodeId) connected.add(e.target);
      if (e.target === highlightNodeId) connected.add(e.source);
    });
    return connected;
  }, [highlightNodeId, edges]);

  const nodesWithHighlight = useMemo(() => {
    return nodes.map(n => ({
      ...n,
      className: highlightNodeId ? (highlightedNodeIds.has(n.id) ? '' : 'dimmed') : ''
    }));
  }, [nodes, highlightNodeId, highlightedNodeIds]);

  const edgesWithHighlight = useMemo(() => {
    return edges.map(e => ({
      ...e,
      className: highlightNodeId ? (e.source === highlightNodeId || e.target === highlightNodeId ? 'highlighted-edge' : 'dimmed-edge') : '',
      animated: highlightNodeId ? (e.source === highlightNodeId || e.target === highlightNodeId) : true,
    }));
  }, [edges, highlightNodeId]);

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
          nodes={nodesWithHighlight}
          edges={edgesWithHighlight}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          onNodeClick={onNodeClick}
          onNodeMouseEnter={onNodeMouseEnter}
          onNodeMouseLeave={onNodeMouseLeave}
          onPaneClick={onPaneClick}
          nodeTypes={nodeTypes}
          fitView
          attributionPosition="bottom-right"
          minZoom={0.1}
        >
          <Background color="#1f2937" gap={24} size={2} />
          <Controls className="custom-controls" />
          <MiniMap
            nodeColor={(n) => {
              if (n.data?.status === 'current') return '#10b981';
              if (n.data?.status === 'stale') return '#f59e0b';
              if (n.data?.status === 'new') return '#3b82f6';
              return '#4b5563';
            }}
            maskColor="rgba(15, 17, 21, 0.7)"
            style={{ backgroundColor: '#1f2937', borderColor: 'rgba(255, 255, 255, 0.1)' }}
          />
        </ReactFlow>

        <AnimatePresence>
          {selectedNodeData && (
            <NodeDetails
              key="node-details"
              data={selectedNodeData}
              onClose={() => setSelectedNodeData(null)}
            />
          )}
        </AnimatePresence>
      </main>
    </div>
  );
}
