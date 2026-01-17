import { getCurrentUser } from './getCurrentUser';

export async function requireTenant(request: Request) {
  const user = await getCurrentUser(request);

  if (!user || !user.tenantId) {
    throw new Response('Unauthorized', { status: 401 });
  }

  return {
    userId: user.id,
    tenantId: user.tenantId
  };
}