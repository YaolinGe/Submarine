""" Cross-covariance models.

"""
import torch
torch.set_default_dtype(torch.float32)


def UniformMixing(gamma0, sigmas):
    """ Create a uniform mixing cross-covariance. 

    Parameters
    ----------
    gamma0: Tensor
        Coupling parameter.
    sigmas: (p) Tensor
        Vector on individual standar deviation for each to the p components.

    Returns
    -------
    function(L1, L2)

    """
    # Convert to tensor if not.
    if not torch.is_tensor(gamma0): gamma0 = torch.tensor(gamma0).float()
    if not torch.is_tensor(sigmas): sigmas = torch.tensor(sigmas).float()

    return lambda L1, L2: _uniform_mixing_crosscov(L1, L2, gamma0, sigmas)

def _uniform_mixing_crosscov(L1, L2, gamma0, sigmas):
    """ Given two vectors of response indices,
    comutes the uniform mixing cross covariance (only response index part).


    Returns
    -------
    gamma: (M, N) Tensor

    """
    # Turn to matrices of size (M, N).
    L1mat, L2mat = torch.meshgrid(L1, L2)
    # Coupling part.
    # Have to extract the float value from gamma0 to use fill.
    gamma_mat = (torch.Tensor(L1mat.shape).fill_(gamma0.item())
            + (1- gamma0) * (L1mat == L2mat))

    # Notice the GENIUS of Pytorch: If we want A_ij to contain sigma[Aij]
    # we just do simga[A] and get the whole matrix, with the same shape as A.
    # This is beautiful.
    sigma_mat1, sigma_mat2 = sigmas[L1mat], sigmas[L2mat]

    return sigma_mat1 * sigma_mat2 * gamma_mat
