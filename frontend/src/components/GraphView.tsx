import { useEffect, useRef, useState } from 'react'
import * as d3 from 'd3'
import type { POI } from '../types/geospatial'

interface Node extends d3.SimulationNodeDatum {
  id: string
  name: string
  type: string
  visited: boolean
}

interface Link extends d3.SimulationLinkDatum<Node> {
  type: string
  strength: number
  distance_m: number
}

interface GraphViewProps {
  pois: POI[]
  visitedPois: Set<string>
  onSelectPOI: (poi: POI) => void
}

export default function GraphView({
  pois,
  visitedPois,
  onSelectPOI,
}: GraphViewProps) {
  const svgRef = useRef<SVGSVGElement>(null)
  const [links, setLinks] = useState<Link[]>([])

  // Calculate relationships
  useEffect(() => {
    const calculatedLinks: Link[] = []

    // Proximity relationships (within 5km)
    for (let i = 0; i < pois.length; i++) {
      for (let j = i + 1; j < pois.length; j++) {
        const p1 = pois[i]
        const p2 = pois[j]
        const dlat = (p2.coordinates[0] - p1.coordinates[0]) * 111
        const dlng =
          (p2.coordinates[1] - p1.coordinates[1]) *
          111 *
          (1 - 0.0066 * ((p1.coordinates[0] + p2.coordinates[0]) / 2))
        const distance = Math.sqrt(dlat * dlat + dlng * dlng) * 1000

        if (distance < 5000) {
          calculatedLinks.push({
            source: p1.id,
            target: p2.id,
            type: 'proximity',
            strength: Math.max(0, 1 - distance / 5000),
            distance_m: Math.round(distance),
          })
        }

        // Same type
        if (p1.type === p2.type) {
          calculatedLinks.push({
            source: p1.id,
            target: p2.id,
            type: 'same_type',
            strength: 0.7,
            distance_m: Math.round(distance),
          })
        }
      }
    }

    setLinks(calculatedLinks)
  }, [pois])

  // D3 visualization
  useEffect(() => {
    if (!svgRef.current || pois.length === 0) return

    const width = svgRef.current.clientWidth
    const height = svgRef.current.clientHeight

    const nodes: Node[] = pois.map((poi) => ({
      id: poi.id,
      name: poi.name,
      type: poi.type,
      visited: visitedPois.has(poi.id),
    }))

    // Create force simulation
    const simulation = d3
      .forceSimulation(nodes as d3.SimulationNodeDatum[])
      .force('link', d3.forceLink<Node, Link>(links as Link[]).id((d) => d.id).distance(100))
      .force('charge', d3.forceManyBody().strength(-300))
      .force('center', d3.forceCenter(width / 2, height / 2))

    const svg = d3.select(svgRef.current)
    svg.selectAll('*').remove()

    const g = svg.append('g')

    // Draw links
    const link = g
      .selectAll('line')
      .data(links)
      .join('line')
      .attr('stroke', (d: any) =>
        d.type === 'proximity' ? '#ccc' : '#e0e0e0'
      )
      .attr('stroke-width', (d: any) => Math.max(1, d.strength * 3))
      .attr('opacity', 0.6)

    // Draw nodes
    const node = g
      .selectAll<SVGCircleElement, Node>('circle')
      .data(nodes)
      .join('circle')
      .attr('r', (d) => (d.visited ? 8 : 6))
      .attr('fill', (d) => {
        const colors: Record<string, string> = {
          scenic: '#2e7d32',
          historical: '#b71c1c',
          food: '#e65100',
          trail: '#1565c0',
          wildlife: '#6a1b9a',
          cultural: '#4e342e',
        }
        return colors[d.type] || '#666'
      })
      .attr('stroke', (d) => (d.visited ? '#fff' : 'none'))
      .attr('stroke-width', 2)
      .style('cursor', 'pointer')
      .on('click', (_, d) => {
        const poi = pois.find((p) => p.id === d.id)
        if (poi) onSelectPOI(poi)
      }) as any

    // Labels
    const labels = g
      .selectAll<SVGTextElement, Node>('text')
      .data(nodes)
      .join('text')
      .attr('font-size', '11px')
      .attr('text-anchor', 'middle')
      .attr('fill', '#333')
      .attr('pointer-events', 'none')
      .text((d) => d.name.substring(0, 10)) as any

    // Drag behavior
    node.call(
      d3.drag<SVGCircleElement, Node>()
        .on('start', (event, d) => {
          if (!event.active) simulation.alphaTarget(0.3).restart()
          d.fx = d.x
          d.fy = d.y
        })
        .on('drag', (event, d) => {
          d.fx = event.x
          d.fy = event.y
        })
        .on('end', (event, d) => {
          if (!event.active) simulation.alphaTarget(0)
          d.fx = null
          d.fy = null
        }) as any
    )

    // Update positions on tick
    simulation.on('tick', () => {
      link
        .attr('x1', (d: any) => (d.source as Node).x || 0)
        .attr('y1', (d: any) => (d.source as Node).y || 0)
        .attr('x2', (d: any) => (d.target as Node).x || 0)
        .attr('y2', (d: any) => (d.target as Node).y || 0)

      node.attr('cx', (d: any) => d.x || 0).attr('cy', (d: any) => d.y || 0)

      labels.attr('x', (d: any) => d.x || 0).attr('y', (d: any) => (d.y || 0) + 14)
    })

    // Zoom
    const zoom = d3.zoom<SVGSVGElement, unknown>().on('zoom', (event) => {
      g.attr('transform', event.transform)
    })
    svg.call(zoom as any)

    return () => {
      simulation.stop()
    }
  }, [pois, links, visitedPois, onSelectPOI])

  return (
    <div className="graph-view">
      <div className="graph-view__header">
        <h2>POI Network Graph</h2>
        <p className="graph-view__hint">
          Drag nodes • Click to select • Zoom/pan the graph
        </p>
      </div>
      <svg ref={svgRef} className="graph-view__svg" />
      <div className="graph-view__legend">
        <div className="legend-item">
          <span className="legend-dot visited" /> Visited
        </div>
        <div className="legend-item">
          <span className="legend-dot unvisited" /> Not visited
        </div>
      </div>
    </div>
  )
}
