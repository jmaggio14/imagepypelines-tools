import { NodeService } from 'rete-angular-render-plugin';

@Injectable({providedIn: 'root'})
export class DashboardService {
    public constructor(protected nodeService: NodeService) {

    }
}