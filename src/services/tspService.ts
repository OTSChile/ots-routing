import { parsePoint } from '../utils/parsePoints';
import { calculateDistance } from '../utils/calculateDistances';
import { getPermutations } from '../services/getPermutations';
import { Point } from '../models/point';

export class TSPService {
    findOptimalRoute(pointsStrList: string[], endPointStr: string) {
        const startPointStr = pointsStrList.shift();
        if (typeof startPointStr === 'undefined') {
            throw new Error('La lista de puntos está vacía');
        }
        const startPoint = parsePoint(startPointStr); // Assume the first point is the start
        const endPoint = parsePoint(endPointStr);
        const points = pointsStrList.map(parsePoint);
      
        let permutations = getPermutations(points);
        let shortestDistance = Infinity;
        let bestRoute: Point[] = []; // Utiliza el tipo Point aquí
        let distances: number[] = []; // Asegúrate de inicializar con un tipo explícito

        permutations.forEach((permutation) => {
            let routeDistance = 0;
            let currentPoint = startPoint;
        
            permutation.forEach((nextPoint: Point) => { // Asegúrate de que nextPoint es de tipo Point
                let dist = calculateDistance(currentPoint, nextPoint);
                distances.push(dist);
                routeDistance += dist;
                currentPoint = nextPoint;
            });
        
            // Add the distance from the last point to the end point
            let distToEnd = calculateDistance(currentPoint, endPoint);
            distances.push(distToEnd);
            routeDistance += distToEnd;
        
            if (routeDistance < shortestDistance) {
                shortestDistance = routeDistance;
                bestRoute = permutation;
            }
        });
      
        // Reconstruct the route with the distances
        let finalRoute = [startPoint, ...bestRoute, endPoint].map(p => `${p.x},${p.y}`);
        let detailedRoute = finalRoute.map((pointStr, i) => {
            if (i === 0) return { point: pointStr, distance: 0 };
            return { point: pointStr, distance: distances[i - 1] };
        });
      
        return {
            shortestDistance,
            detailedRoute,
        };
    }
}
